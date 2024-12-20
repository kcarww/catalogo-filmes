from uuid import UUID
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT
)

from core._shared.events.message_bus import MessageBus
from core._shared.infrastructure.storage.local_storage import LocalStorage
from core.video.application.use_cases.create_video_without_media import CreateVideoWithoutMedia
from core.video.application.use_cases.delete_video_use_case import DeleteVideo, DeleteVideoRequest
from core.video.application.use_cases.exceptions import VideoNotFound
from core.video.application.use_cases.get_video_use_case import GetVideo, GetVideoRequest
from core.video.application.use_cases.list_video_use_case import ListVideo, ListVideoRequest
from core.video.application.use_cases.upload_video import UploadVideo
from django_project.cast_member_app.repository import DjangoORMCastMemberRepository
from django_project.category_app.repository import DjangoORMCategoryRepository
from django_project.genre_app.repository import DjangoORMGenreRepository
from django_project.video_app.repository import DjangoORMVideoRepository
from django_project.video_app.serializers import CreateVideoRequestSerializer, CreateVideoResponseSerializer, DeleteVideoRequestSerializer, ListVideoResponseSerializer, RetrieveVideoRequestSerializer, RetrieveVideoResponseSerializer

class VideoViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        order_by = request.query_params.get("order_by", "title")
        current_page = request.query_params.get("current_page", 1)
        input = ListVideoRequest(order_by=order_by, current_page=int(current_page))
        use_case = ListVideo(repository=DjangoORMVideoRepository())
        output = use_case.execute(input)
        
        serializer = ListVideoResponseSerializer(output)
        return Response(
            status=HTTP_200_OK,
            data=serializer.data
        )
    
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
        
    def retrieve(self, request: Request, pk: UUID = None) -> Response:
        serializer = RetrieveVideoRequestSerializer(data={"id": pk})
        serializer.is_valid(raise_exception=True)
        
        use_case = GetVideo(repository=DjangoORMVideoRepository())
        try:
            result = use_case.execute(request=GetVideoRequest(id=serializer.validated_data["id"])) # type: ignore
        except VideoNotFound:
            return Response(HTTP_404_NOT_FOUND)
        
        video_output = RetrieveVideoResponseSerializer(instance=result)

        return Response(
            status=HTTP_200_OK,
            data=video_output.data
        )
        
    def update(self, request: Request, pk: UUID = None):
        raise NotImplementedError
    
    def partial_update(self, request: Request, pk: UUID = None):
        file = request.FILES["video_file"] # type: ignore
        content = file.read() # type: ignore
        content_type = file.content_type # type: ignore

        upload_video = UploadVideo(
            repository=DjangoORMVideoRepository(),
            storage_service=LocalStorage(),
            message_bus=MessageBus()
        )
        try:
            upload_video.execute(
                UploadVideo.Input(
                    video_id=pk,
                    file_name=file.name, # type: ignore
                    content=content,
                    content_type=content_type # type: ignore
                )
            )
        except VideoNotFound:
            return Response(status=404)

        return Response(status=200)
    
    def destroy(self, request: Request, pk: UUID = None):
        serializer = DeleteVideoRequestSerializer(data={"id": pk})
        serializer.is_valid(raise_exception=True)
        
        use_case = DeleteVideo(repository=DjangoORMVideoRepository())
        try:
            use_case.execute(request=DeleteVideoRequest(id=serializer.validated_data["id"])) # type: ignore
        except VideoNotFound:
            return Response(HTTP_404_NOT_FOUND)
        
        return Response(status=HTTP_204_NO_CONTENT)
        
        