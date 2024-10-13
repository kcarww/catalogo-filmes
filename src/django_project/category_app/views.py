from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

class CategoryViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        return Response(status=HTTP_200_OK,
                        data=[
                            {
                                "id": "a5b518c3-a34a-459a-b33f-c986e1f62114",
                                "name": "Movie",
                                "description": "Movies category",
                                "is_active": True
                            },
                            {
                                "id": "18836c68-c71d-4346-b545-37f6205f09c9",
                                "name": "Movie 2",
                                "description": "Movies category",
                                "is_active": False
                            }   
                        ]
                        )