from django.urls import path
from .views import StartFederatedLearningView, FederatedLearningResultListView, FederatedLearningResultRetrieveView

urlpatterns = [
    # URL for starting federated learning process
    path('start_federated_learning/<int:client_data_id>/', StartFederatedLearningView.as_view(), name='start_federated_learning'),

    # URL for listing federated learning results based on data_id
    path('federated_learning_results/<str:data_id>/', FederatedLearningResultListView.as_view(), name='federated_learning_results_list'),

    # URL for retrieving a specific federated learning result for a given data_id
    path('federated_learning_results/<str:data_id>/latest/', FederatedLearningResultRetrieveView.as_view(), name='federated_learning_result_retrieve'),
]
