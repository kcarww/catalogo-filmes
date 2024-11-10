from uuid import UUID
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from core.category.application.use_cases.create_category import CreateCategory, CreateCategoryRequest, CreateCategoryResponse
from core.category.application.use_cases.delete_category import DeleteCategory, DeleteCategoryRequest
from core.category.application.use_cases.exceptions import CategoryNotFound
from core.category.application.use_cases.get_category import GetCategory, GetCategoryRequest
from core.category.application.use_cases.list_category import ListCategory, ListCategoryRequest
from core.category.application.use_cases.update_category import UpdateCategory, UpdateCategoryRequest
from django_project.category_app import serializers
from django_project.category_app.repository import DjangoORMCategoryRepository
from django_project.category_app.serializers import  CreateCategoryRequestSerializer, CreateCategoryResponseSerializer, DeleteCategoryRequestSerializer, ListCategoryResponseSerializer, RetrieveCategoryRequestSerializer, RetrieveCategoryResponseSerializer, UpdateCategoryRequestSerializer


class CategoryViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        input = ListCategoryRequest()
        use_case = ListCategory(repository=DjangoORMCategoryRepository())
        output = use_case.execute(input)

        serializer = ListCategoryResponseSerializer(instance=output)

        return Response(status=status.HTTP_200_OK,
                        data=serializer.data
                        )

    def retrieve(self, request: Request, pk=None):
        serializer = RetrieveCategoryRequestSerializer(data={"id": pk})
        serializer.is_valid(raise_exception=True)

        use_case = GetCategory(repository=DjangoORMCategoryRepository())

        try:
            result = use_case.execute(request=GetCategoryRequest(
                id=serializer.validated_data["id"]))
        except CategoryNotFound:
            return Response(status=status.HTTP_404_NOT_FOUND)

        category_output = RetrieveCategoryResponseSerializer(instance=result)

        return Response(
            status=status.HTTP_200_OK,
            data=category_output.data
        )
        
    def create(self, request: Request) -> Response:
        serializer = CreateCategoryRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        category_input = CreateCategoryRequest(**serializer.validated_data) # type: ignore
        use_case = CreateCategory(repository=DjangoORMCategoryRepository())
        category_output = use_case.execute(request=category_input)
        
        return Response(
            status=status.HTTP_201_CREATED,
            data=CreateCategoryResponseSerializer(instance=category_output).data
        )
        
    def update(self, request: Request, pk: UUID = None) -> Response: # type: ignore
        serializer = UpdateCategoryRequestSerializer(
            data={
                **request.data, # type: ignore
                "id": pk
            }
        )
        serializer.is_valid(raise_exception=True)
        category_input = UpdateCategoryRequest(**serializer.validated_data) # type: ignore
        use_case = UpdateCategory(repository=DjangoORMCategoryRepository())
        try: 
            use_case.execute(request=category_input)
        except CategoryNotFound:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request: Request, pk=None) -> Response:
        serializer = DeleteCategoryRequestSerializer(data={"id": pk})
        serializer.is_valid(raise_exception=True)
        
        use_case = DeleteCategory(repository=DjangoORMCategoryRepository())
        try:
            use_case.execute(request=DeleteCategoryRequest(
                **serializer.validated_data # type: ignore
            ))
        except CategoryNotFound:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)