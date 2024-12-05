import logging
from typing import Type
from core._shared.application.handler import Handler
from core._shared.events.abstract_message_bus import AbstractMessageBus
from core._shared.events.event import Event
from core._shared.infrastructure.events.rabbitmq_dispatcher import RabbitMQDispatcher
from core.video.application.events.handlers import DummyHandler, PublishAudioVideoMediaUpdatedHandler
from core.video.application.events.integration_events import AudioVideoMediaUpdatedIntegrationEvent
from core.video.domain.events.events import AudioVideoMediaUpdated

logger = logging.getLogger(__name__)

class MessageBus(AbstractMessageBus):
    def __init__(self) -> None:
        self.handlers: dict[Type[Event], list[Handler]] = {
            AudioVideoMediaUpdatedIntegrationEvent: [
                PublishAudioVideoMediaUpdatedHandler(dispatcher=RabbitMQDispatcher(queue="videos.new")),
            ],
            AudioVideoMediaUpdated: [
                DummyHandler(),
            ],
        }
    
    def handle(self, events: list[Event]) -> None:
        for event in events:
            handlers = self.handlers.get(type(event), [])
            for handler in self.handlers[type(event)]:
                try:
                    handler.handle(event)
                except Exception as e:
                    logger.exception("Exception handling event %s", event)
                    continue