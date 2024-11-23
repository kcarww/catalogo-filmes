from uuid import UUID
from django.db import transaction

from core.video.domain.value_objects import AudioVideoMedia
from core.video.domain.video import Video
from core.video.domain.video_repository import VideoRepository
from django_project.video_app.models import Video as VideoModel

class DjangoORMVideoRepository(VideoRepository):
    def save(self, video: Video) -> None:
        with transaction.atomic():
            video_model = VideoModel(
                title=video.title,
                description=video.description,
                launch_year=video.launch_year,
                duration=video.duration,
                published=video.published,
                rating=video.rating                
            )
            
            video_model.categories.set(video.categories)
            video_model.genres.set(video.genres)
            video_model.cast_members.set(video.cast_members)


class VideoModelMapper:
    @staticmethod
    def to_entity(model: VideoModel) -> Video:
        video =  Video(
            id=model.id,
            title=model.title,
            description=model.description,
            launch_year=model.launch_year,
            duration=model.duration,
            rating=model.rating,
            published=model.published,
            categories=set(model.categories.values_list("id", flat=True)),
            genres=set(model.genres.values_list("id", flat=True)),
            cast_members=set(model.cast_members.values_list("id", flat=True)),
        )
        
        if model.video:
            video.video = AudioVideoMedia(
                id=model.video.id,
                name=model.video.name,
                raw_location=model.video.raw_location,
                encoded_location=model.video.encoded_location,
                status=model.video.status,
                check_sum=model.video.check_sum,
            )
        
        return video