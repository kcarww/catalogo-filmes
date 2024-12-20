from decimal import Decimal
from pathlib import Path
from unittest.mock import create_autospec

from core._shared.events.abstract_message_bus import AbstractMessageBus
from core._shared.infrastructure.storage.abstract_storage import AbstractStorage
from core.video.application.events.integration_events import AudioVideoMediaUpdatedIntegrationEvent
from core.video.application.use_cases.upload_video import UploadVideo
from core.video.domain.value_objects import AudioVideoMedia, MediaStatus, MediaType, Rating
from core.video.domain.video import Video
from core.video.infra.in_memory_video_repository import InMemoryVideoRepository


class TestUploadVideo:
    def test_upload_video_media_to_video(self):
        video = Video(
            title="Video 1",
            description="Video 1 description",
            launch_year=2021,
            duration=Decimal(120),
            rating=Rating.AGE_14,
            opened=True,
            cast_members=set(),
            categories=set(),
            genres=set(),
        )
        
        video_repository = InMemoryVideoRepository(videos=[video])
        mock_storage = create_autospec(AbstractStorage)
        mock_message_bus = create_autospec(AbstractMessageBus)
        use_case = UploadVideo(
            repository=video_repository,
            storage_service=mock_storage,
            message_bus=mock_message_bus
        )

        use_case.execute(
            UploadVideo.Input(
                video_id=video.id,
                file_name="video.mp4",
                content=b"video content",
                content_type="video/mp4",
            )
        )
        mock_storage.store.assert_called_once_with(
            file_path=Path(f"videos/{video.id}/video.mp4"),
            content=b"video content",
            content_type="video/mp4",
        )
        
        
        assert video.video == AudioVideoMedia(
            id=video.video.id,
            name="video.mp4",
            raw_location=str(Path(f"videos/{video.id}/video.mp4")),
            encoded_location="",
            status=MediaStatus.PENDING,
        )
        assert video_repository.videos[0] == video

        mock_message_bus.handle.assert_called_once_with([
            AudioVideoMediaUpdatedIntegrationEvent(
                resource_id=f"{str(video.id)}.{MediaType.VIDEO}",
                file_path=str(Path(f"videos/{video.id}/video.mp4")),
            )
        ])