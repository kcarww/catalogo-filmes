from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from core.video.application.use_cases.exceptions import VideoNotFound
from core.video.domain.value_objects import AudioVideoMedia, ImageMedia, Rating
from core.video.domain.video_repository import VideoRepository


@dataclass
class GetVideoRequest:
    id: UUID
    
@dataclass
class GetVideoResponse:
    id: UUID
    title: str
    description: str
    launch_year: int
    duration: Decimal
    published: bool
    rating: Rating
    
    categories: set[UUID]
    genres: set[UUID]
    cast_members: set[UUID]
    
    banner: ImageMedia | None = None
    thumbnail: ImageMedia | None = None
    thumbnail_half: ImageMedia | None = None
    trailer: AudioVideoMedia | None = None
    video: AudioVideoMedia | None = None
    

class GetVideo:
    def __init__(self, repository: VideoRepository):
        self.repository = repository
        
    def execute(self, request: GetVideoRequest) -> GetVideoResponse:
        video = self.repository.get_by_id(id=request.id)
        
        if video is None:
            raise VideoNotFound(f"Video with {request.id} not found")
        
        return GetVideoResponse(
            id=video.id,
            title=video.title,
            description=video.description,
            launch_year=video.launch_year,
            duration=video.duration,
            published=video.published,
            rating=video.rating,
            categories=video.categories,
            genres=video.genres,
            cast_members=video.cast_members,
            banner=video.banner,
            thumbnail=video.thumbnail,
            thumbnail_half=video.thumbnail_half,
            trailer=video.trailer,
            video=video.video,
        )