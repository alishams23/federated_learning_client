from django.shortcuts import render

# Create your views here.
from django_filters import rest_framework as filterSpecial  

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from client_model.tasks import start_federated_learning
from .models import ClientData
from .serializers import ClientDataSerializer
from rest_framework import generics, filters
from .paginations import ClientDataPagination
from django_filters import rest_framework as django_filters
from .filters import ClientDataFilter
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse

@login_required
def generating_model(request, id):
    app_name = "client_data"
    model_name = "clientdata"
    admin_url = reverse(f'admin:{app_name}_{model_name}_changelist')  # Admin list view URL
    data = ClientData.objects.get(id=id)
    data.status = "pending" 
    data.save()
    for item in range(0,2):
        print(item)
        start_federated_learning.apply_async(args=[data.id, data.uploaded_file.path])
    return redirect(admin_url)


class DataUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        serializer = ClientDataSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            return Response({"message": "File uploaded successfully","id":instance.id}, status=201)
        return Response(serializer.errors, status=400)
    
    
class ClientDataListView(generics.ListAPIView):
    queryset = ClientData.objects.all()
    serializer_class = ClientDataSerializer
    pagination_class = ClientDataPagination
    filter_backends = (filters.OrderingFilter, filters.SearchFilter, filterSpecial.DjangoFilterBackend)
    filterset_class = ClientDataFilter  # Enable filtering
    search_fields = ['description']  # Enable searching by description
    ordering_fields = ['upload_time', 'status']  # Allow ordering by these fields
    ordering = ['-upload_time']  # Default ordering (descending by upload_time)