from django.urls import path
from .views import DataUploadView ,ClientDataListView ,generating_model

app_name = 'client_data'
urlpatterns = [
    # URL for starting federated learning process
     path('start-generating-model/<int:id>/', generating_model, name='generating_model'),
    path('data-create/', DataUploadView.as_view(), name='start_federated_learning'),
    path('data-list/', ClientDataListView.as_view(), name='start_federated_learning'),
]
