from rest_framework.pagination import PageNumberPagination

class FederatedLearningResultPagination(PageNumberPagination):
    page_size = 20  # Number of results per page
    page_size_query_param = 'page_size'
    max_page_size = 100