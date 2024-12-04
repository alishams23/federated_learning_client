import subprocess
import json
from client_model.flower_client_script import start_client
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ClientData, FederatedLearningResult
from .serializers import FederatedLearningResultSerializer
from rest_framework import generics
# Create your views here.
from django.http import JsonResponse
from .tasks import start_federated_learning

class StartFederatedLearningView(APIView):
    def get(self, request, client_data_id):
        try:
            # Retrieve the client data
            client_data = ClientData.objects.get(id=client_data_id)

            # Check if the client data is processed already
            if client_data.status != 'processed':
                # Call the Celery task to run in the background
                start_federated_learning.apply_async(args=[client_data.id, client_data.uploaded_file.path])

                # Return a response indicating the task has been started
                return JsonResponse({
                    "message": "Federated learning started successfully, results will be processed in the background."
                })
            else:
                return JsonResponse({"message": "Client data already processed"}, status=400)

        except ClientData.DoesNotExist:
            return JsonResponse({"error": "Client data not found"}, status=404)
        
class FederatedLearningResultListView(generics.ListAPIView):
    serializer_class = FederatedLearningResultSerializer

    def get_queryset(self):
        data_id = self.kwargs['data_id']
        return FederatedLearningResult.objects.filter(data__id=data_id).order_by('-processed_time')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset.exists():
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        return Response({"message": "No results found for this data"}, status=404)

class FederatedLearningResultRetrieveView(generics.RetrieveAPIView):
    queryset = FederatedLearningResult.objects.all()
    serializer_class = FederatedLearningResultSerializer

    def get_object(self):
        data_id = self.kwargs['data_id']
        return FederatedLearningResult.objects.filter(data__id=data_id).order_by('-processed_time').first()
    
    def retrieve(self, request, *args, **kwargs):
        result = self.get_object()
        if result:
            serializer = self.get_serializer(result)
            return Response(serializer.data)
        return Response({"message": "No results found for this client"}, status=404)