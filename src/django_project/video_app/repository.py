from base64 import encode
from uuid import UUID
from django.db import transaction

from core.video.domain.value_objects import AudioVideoMedia
from core.video.domain.video import Video
from core.video.domain.video_repository import VideoRepository
from django_project.video_app.models import Video as VideoModel, AudioVideoMedia as AudioVideoMediaModel

class DjangoORMVideoRepository(VideoRepository):
    def save(self, video: Video) -> None:
        with transaction.atomic():
            video_model = VideoModel(
                title=video.title,
                description=video.description,
                launch_year=video.launch_year,
                opened=video.opened,
                duration=video.duration,
                published=video.published,
                rating=video.rating                
            )
            video_model.save()
            
            video_model.categories.set(video.categories)
            video_model.genres.set(video.genres)
            video_model.cast_members.set(video.cast_members)
            video_model.save()
            
    
    def get_by_id(self, id: UUID) -> Video:
        try:
            model = VideoModel.objects.get(id=id)
        except VideoModel.DoesNotExist:
            return None # type: ignore
        else:
            return VideoModelMapper.to_entity(model)
        
    def delete(self, id: UUID) -> None:
        VideoModel.objects.filter(id=id).delete()
        
    def list(self) -> list[Video]:
        return [VideoModelMapper.to_entity(model) for model in VideoModel.objects.all()]
    
    def update(self, video: Video) -> None:
        with transaction.atomic():
            try:
                video_model = VideoModel.objects.get(pk=video.id)
                
            except VideoModel.DoesNotExist:
                return None
            else:
                with transaction.atomic():
                    AudioVideoMediaModel.objects.filter(id=video_model.video_id).delete() # type: ignore
                    video_model.video = AudioVideoMediaModel.objects.create( # type: ignore
                        name=video.video.name,
                        raw_location=video.video.raw_location,
                        encoded_location=video.video.encoded_location,
                        status=video.video.status,
                    ) if video.video else None

                    
                    video_model.categories.set(video.categories)
                    video_model.genres.set(video.genres)
                    video_model.cast_members.set(video.cast_members)
                    
                    video_model.title = video.title
                    video_model.description = video.description
                    video_model.launch_year = video.launch_year
                    video_model.opened = video.opened
                    video_model.duration = video.duration
                    video_model.rating = video.rating # type: ignore
                    video_model.published = video.published

                    video_model.save()

class VideoModelMapper:
    @staticmethod
    def to_entity(model: VideoModel) -> Video:
        video =  Video(
            id=model.id,
            title=model.title,
            description=model.description,
            launch_year=model.launch_year,
            opened=model.opened,
            duration=model.duration,
            rating=model.rating, # type: ignore
            categories=set(model.categories.values_list("id", flat=True)),
            genres=set(model.genres.values_list("id", flat=True)),
            cast_members=set(model.cast_members.values_list("id", flat=True)),
        )
        
        if model.video:
            video.video = AudioVideoMedia(
                name=model.video.name,
                raw_location=model.video.raw_location,
                encoded_location=model.video.encoded_location,
                status=model.video.status,
            )
        
        return video