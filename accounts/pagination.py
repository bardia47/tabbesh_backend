from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class Pagination(PageNumberPagination):
    def get_paginated_response(self, data):
        #add pages count to response header
        return Response( data,headers={"Last-Page" : self.page.paginator.num_pages})