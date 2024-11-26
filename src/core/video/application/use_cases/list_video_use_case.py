from abc import ABC
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Generic, TypeVar
from uuid import UUID
import config
from core.video.domain.value_objects import AudioVideoMedia, ImageMedia, Rating
from core.video.domain.video_repository import VideoRepository


@dataclass
class ListVideoRequest:
    order_by: str = "title"
    current_page: int = 1
    
@dataclass
class ListVideoOutput:
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
    

@dataclass
class ListVideoOutputMeta:
    current_page: int = 1
    per_page: int = config.DEFAULT_PAGINATION_SIZE
    total: int = 0
    
T = TypeVar("T")

@dataclass
class ListVideoResponse(Generic[T], ABC):
    data: list[T]
    meta: ListVideoOutputMeta = field(default_factory=ListVideoOutputMeta)
    

class ListVideo:
    def __init__(self, repository: VideoRepository):
        self.repository = repository
        
    
    def execute(self, request: ListVideoRequest) -> ListVideoResponse:
        videos = self.repository.list()
        sorted_videos = sorted([
            ListVideoOutput(
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
            for video in videos
        ], key=lambda video: getattr(video, request.order_by))
        
        page_offset = (request.current_page - 1) * config.DEFAULT_PAGINATION_SIZE
        videos_page = sorted_videos[page_offset:page_offset + config.DEFAULT_PAGINATION_SIZE]
        
        return ListVideoResponse(
            data=videos_page,
            meta=ListVideoOutputMeta(
                current_page=request.current_page,
                per_page=config.DEFAULT_PAGINATION_SIZE,
                total=len(sorted_videos)
            )
        )