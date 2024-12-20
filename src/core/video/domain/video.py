from dataclasses import dataclass, field
from decimal import Decimal
from uuid import UUID
from core._shared.domain.entity import Entity
from core.video.domain.value_objects import AudioVideoMedia, ImageMedia, MediaStatus, Rating

@dataclass(slots=True, kw_only=True)
class Video(Entity):
    title: str
    description: str
    launch_year: int
    duration: Decimal
    opened: bool
    published: bool = field(default=False, init=False)
    rating: Rating
    
    categories: set[UUID]
    genres: set[UUID]
    cast_members: set[UUID]
    
    banner: ImageMedia | None = None
    thumbnail: ImageMedia | None = None
    thumbnail_half: ImageMedia | None = None
    trailer: AudioVideoMedia | None = None
    video: AudioVideoMedia | None = None
    
    # TODO: adicionar atributos de media
    
    def __post_init__(self):
        self.validate()
        
    def validate(self):
        if len(self.title) > 255:
            self.notification.add_error("title must have less than 256 characteres")
            
        if self.notification.has_errors:
            raise ValueError(self.notification.messages)
        
    def update(
        self,
        title: str,
        description: str,
        launch_year: int,
        duration: Decimal,
        published: bool,
        rating: Rating,
    ) -> None:
        self.title = title
        self.description = description
        self.launch_year = launch_year
        self.duration = duration
        self.rating = rating
        self.published = published
        
        self.validate()
        
    def publish(self) -> None:
        if not self.video:
            self.notification.add_error("Video media is required to publish the video")
        elif self.video.status != MediaStatus.COMPLETED:
            self.notification.add_error("Video must be fully processed to be published")

        self.published = True
        self.validate()
        
    def add_category(self, category_id: UUID) -> None:
        self.categories.add(category_id)
        
    def add_genre(self, genre_id: UUID) -> None:
        self.genres.add(genre_id)
        
    def add_cast_member(self, cast_member_id: UUID) -> None:
        self.cast_members.add(cast_member_id)
        
    def update_banner(self, banner: ImageMedia) -> None:
        self.banner = banner
        self.validate()

    def update_thumbnail(self, thumbnail: ImageMedia) -> None:
        self.thumbnail = thumbnail
        self.validate()

    def update_thumbnail_half(self, thumbnail_half: ImageMedia) -> None:
        self.thumbnail_half = thumbnail_half
        self.validate()

    def update_video_media(self, video: AudioVideoMedia) -> None:
        self.video = video
        self.validate()

    def update_trailer(self, trailer: AudioVideoMedia) -> None:
        self.trailer = trailer
        self.validate()

    def process(self, status: MediaStatus, encoded_location: str = "") -> None:
        if status == MediaStatus.COMPLETED:
            self.video = self.video.complete(encoded_location) # type: ignore
            self.publish()
        else:
            self.video = self.video.fail() # type: ignore

        self.validate()
