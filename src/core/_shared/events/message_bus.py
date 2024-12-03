from typing import Type
from core._shared.application.handler import Handler
from core._shared.events.abstract_message_bus import AbstractMessageBus
from core._shared.events.event import Event

class MessageBus(AbstractMessageBus):
    def __init__(self) -> None:
        self.handlers: dict[Type[Event], list[Handler]] = {}
    
    def handle(self, events: list[Event]) -> None:
        for event in events:
            handlers = self.handlers.get(type(event), [])
            for handler in self.handlers[type(event)]:
                try:
                    handler.handle(event)
                except Exception as e:
                    print(e)