from rest_framework.pagination import PageNumberPagination

class ClientDataPagination(PageNumberPagination):
    page_size = 10  # Define how many items per page
    page_size_query_param = 'page_size'
    max_page_size = 100  # Define a maximum page size limit
