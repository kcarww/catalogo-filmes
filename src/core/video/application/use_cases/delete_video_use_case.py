from dataclasses import dataclass
from uuid import UUID

from core.video.application.use_cases.exceptions import VideoNotFound
from core.video.domain.video_repository import VideoRepository

@dataclass
class DeleteVideoRequest:
    id: UUID
    
class DeleteVideo:
    def __init__(self, repository: VideoRepository):
        self.repository = repository
        
    def execute(self, request: DeleteVideoRequest) -> None:
        video = self.repository.get_by_id(request.id)
        if video is None:
            raise VideoNotFound(f"Video with id {request.id} not found")
        
        self.repository.delete(request.id)