from core._shared.events.abstract_message_bus import AbstractMessageBus
from core._shared.events.event import Event

class MessageBus(AbstractMessageBus):
    def handle(self, events: list[Event]) -> None:
        print("Handling events", events)
        