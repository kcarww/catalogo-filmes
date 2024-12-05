from dataclasses import dataclass
from uuid import UUID

from core.video.application.use_cases.exceptions import MediaNotFound, VideoNotFound
from core.video.domain.value_objects import MediaStatus, MediaType
from core.video.domain.video_repository import VideoRepository


class ProcessAudioVideoMedia:

    @dataclass
    class Input:
        encoded_location: str
        video_id: UUID
        status: MediaStatus
        media_type: MediaType

    def __init__(self, video_repository: VideoRepository):
        self.video_repository = video_repository

    def execute(self, request: Input):
        video = self.video_repository.get_by_id(request.video_id)
        if video is None:
            raise VideoNotFound(f"Video with id {request.video_id} not found")
        
        if request.media_type == MediaType.VIDEO:
            if not video.video:
                raise MediaNotFound("Video must have media to be processed")
        
            video.process(status=request.status, encoded_location=request.encoded_location)

        self.video_repository.update(video)