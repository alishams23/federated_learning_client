from django.urls import path
from .views import DataUploadView ,ClientDataListView

urlpatterns = [
    # URL for starting federated learning process
    path('data-create/', DataUploadView.as_view(), name='start_federated_learning'),
    path('data-list/', ClientDataListView.as_view(), name='start_federated_learning'),
]
