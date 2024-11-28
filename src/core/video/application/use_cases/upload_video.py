from dataclasses import dataclass
from pathlib import Path
from uuid import UUID

from core._shared.infrastructure.storage.abstract_storage import AbstractStorage
from core.video.application.use_cases.exceptions import VideoNotFound
from core.video.domain.value_objects import AudioVideoMedia, MediaStatus
from core.video.domain.video_repository import VideoRepository


class UploadVideo:
    @dataclass
    class Input:
        video_id: UUID
        file_name: str
        content: bytes
        content_type: str
        
    def __init__(self, repository: VideoRepository, storage_service: AbstractStorage):
        self.repository = repository
        self.storage_service = storage_service
        
    def execute(self, input: Input):
        video = self.repository.get_by_id(input.video_id)
        if not video:
            raise VideoNotFound(input.video_id)
        
        file_path = Path("videos") / str(video.id) / input.file_name
        self.storage_service.store(
            file_path=file_path, # type: ignore
            content=input.content,
            content_type=input.content_type
            )
        
        audio_video_media = AudioVideoMedia(
            name=input.file_name,
            raw_location=str(file_path),
            encoded_location="",
            status=MediaStatus.PENDING
        )
        
        video.update_video_media(audio_video_media)
        self.repository.update(video)
        