import re
from uuid import UUID
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

from core.cast_member.application.use_cases.create_cast_member import CreateCastMember, CreateCastMemberRequest, CreateCastMemberResponse
from core.cast_member.application.use_cases.delete_cast_member import DeleteCastMember, DeleteCastMemberRequest
from core.cast_member.application.use_cases.exceptions import CastMemberNotFound, InvalidCastMember
from core.cast_member.application.use_cases.list_cast_member_use_case import ListCastMemberOutput, ListCastMemberRequest, ListCastMemberUseCase
from core.cast_member.application.use_cases.update_cast_member_use_case import UpdateCastMember, UpdateCastMemberRequest
from django_project.cast_member_app.repository import DjangoORMCastMemberRepository
from django_project.cast_member_app.serializers import CreateCastMemberRequestSerializer, CreateCastMemberResponseSerializer, DeleteCastMemberRequestSerializer, ListCastMembersResponseSerializer, RetrieveCastMemberRequestSerializer, UpdateCastMemberRequestSerializer

class CastMemberViewSet(viewsets.ViewSet):
    def create(self, request: Request) -> Response:
        serializer = CreateCastMemberRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        cast_member_input = CreateCastMemberRequest(**serializer.validated_data) # type: ignore
        use_case = CreateCastMember(repository=DjangoORMCastMemberRepository())
        cast_member_output = use_case.execute(cast_member_input)
        
        return Response(
            status=HTTP_201_CREATED,
            data=CreateCastMemberResponseSerializer(instance=cast_member_output).data
        )
        
        
    def list(self, request: Request) -> Response:
        use_case = ListCastMemberUseCase(repository=DjangoORMCastMemberRepository())
        output: ListCastMemberOutput = use_case.execute(ListCastMemberRequest())
        response_serializer = ListCastMembersResponseSerializer(output)
        return Response(
            status=HTTP_200_OK,
            data=response_serializer.data
        )
    def retrieve(self, request: Request, pk: str) -> Response:
        serializer = RetrieveCastMemberRequestSerializer(data={"id": pk})
        serializer.is_valid(raise_exception=True)
        
        # TODO - TERMINAR O GET CAST MEMBER
        return Response()
    
    def update(self, request: Request, pk: UUID) -> Response:
        serializer = UpdateCastMemberRequestSerializer(
            data={
                "id": pk,
                **request.data # type: ignore
            }
        )
        serializer.is_valid(raise_exception=True)
        
        input = UpdateCastMemberRequest(**serializer.validated_data) # type: ignore
        use_case = UpdateCastMember(repository=DjangoORMCastMemberRepository())
        try:
            use_case.execute(input)
        except CastMemberNotFound as e:
            return Response(
                status=HTTP_404_NOT_FOUND
            )
        except InvalidCastMember as e:
            return Response(
                status=HTTP_400_BAD_REQUEST,
                data={"error": str(e)}
            )
        return Response(status=HTTP_204_NO_CONTENT)
    
    def destroy(self, request: Request, pk: str) -> Response:
        serializer = DeleteCastMemberRequestSerializer(data={"id": pk})
        serializer.is_valid(raise_exception=True)
        
        input = DeleteCastMemberRequest(**serializer.validated_data) # type: ignore
        use_case = DeleteCastMember(repository=DjangoORMCastMemberRepository())
        
        try:
            use_case.execute(input)
        except CastMemberNotFound as e:
            return Response(
                status=HTTP_404_NOT_FOUND
            )
        return Response(status=HTTP_204_NO_CONTENT)
