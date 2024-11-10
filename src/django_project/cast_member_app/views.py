from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_201_CREATED,
)

from core.cast_member.application.use_cases.list_cast_member_use_case import ListCastMemberOutput, ListCastMemberRequest, ListCastMemberUseCase
from django_project.cast_member_app.repository import DjangoORMCastMemberRepository
from django_project.cast_member_app.serializers import ListCastMembersResponseSerializer

class CastMemberViewSet(viewsets.ViewSet):
    def create(self, request: Request) -> Response:
        pass
    
    def list(self, request: Request) -> Response:
        use_case = ListCastMemberUseCase(repository=DjangoORMCastMemberRepository())
        output: ListCastMemberOutput = use_case.execute(ListCastMemberRequest())
        response_serializer = ListCastMembersResponseSerializer(output)
        return Response(
            status=HTTP_200_OK,
            data=response_serializer.data
        )
    def retrieve(self, request: Request, pk: str) -> Response:
        pass
    
    def update(self, request: Request, pk: str) -> Response:
        pass
    
    def destroy(self, request: Request, pk: str) -> Response:
        pass
