from uuid import UUID
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_201_CREATED,
)

from core.video.application.use_cases.create_video_without_media import CreateVideoWithoutMedia
from django_project.cast_member_app.repository import DjangoORMCastMemberRepository
from django_project.category_app.repository import DjangoORMCategoryRepository
from django_project.genre_app.repository import DjangoORMGenreRepository
from django_project.video_app.repository import DjangoORMVideoRepository
from django_project.video_app.serializers import CreateVideoRequestSerializer, CreateVideoResponseSerializer

class VideoViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        raise NotImplementedError
    
    def create(self, request: Request) -> Response:
        serializer = CreateVideoRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        input = CreateVideoWithoutMedia.Input(
            **serializer.validated_data # type: ignore
        )
        use_case = CreateVideoWithoutMedia(
            video_repository=DjangoORMVideoRepository(),
            category_repository=DjangoORMCategoryRepository(),
            cast_member_repository=DjangoORMCastMemberRepository(),
            genre_repository=DjangoORMGenreRepository()) # type: ignore
        output = use_case.execute(input)
        
        return Response(
            status=HTTP_201_CREATED,
            data=CreateVideoResponseSerializer(output).data
        )
        
    def update(self, request: Request, pk: UUID = None):
        raise NotImplementedError
    
    def partial_update(self, request: Request, pk: UUID = None):
        raise NotImplementedError
    
    def destroy(self, request: Request, pk: UUID = None):
        raise NotImplementedError
        
        