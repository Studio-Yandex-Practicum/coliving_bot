from rest_framework.pagination import PageNumberPagination


class UsersResultsSetPagination(PageNumberPagination):
    page_size = 100
