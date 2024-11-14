from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from core._shared.domain.entity import Entity

@dataclass
class Video(Entity):
    title: str
    description: str
    launch_year: int
    duration: Decimal
    published: bool
    rating: Rating
    
    categories: set[UUID]
    genres: set[UUID]
    cast_member: set[UUID]
    
    # TODO: adicionar atributos de media
    
    def __post_init__(self):
        self.validate()
        
    def validate(self):
        if len(self.title) > 255:
            self.notification.add_error("title must have less than 256 characteres")
            
        if self.notification.has_errors:
            raise ValueError(self.notification.messages)