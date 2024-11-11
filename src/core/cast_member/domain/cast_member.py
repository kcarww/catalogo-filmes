from enum import StrEnum
from dataclasses import field, dataclass
import uuid
from uuid import UUID

from core._shared.domain.entity import Entity

class CastMemberType(StrEnum):
    DIRECTOR = 'DIRECTOR'
    ACTOR = 'ACTOR'
    
    
@dataclass(eq=False)
class CastMember(Entity):
    name: str
    type: CastMemberType
    
    def __post_init__(self):
        self.validate()
    
    def validate(self):
        if len(self.name) > 255:
            # raise ValueError('name cannot be longer than 255')
            self.notification.add_error('name cannot be longer than 255')
        
        if not self.name:
            self.notification.add_error('name cannot be empty')
            # raise ValueError('name cannot be empty')
        
        if not self.type in CastMemberType:
            # raise ValueError('type must be a valid CastMemberType: actor or director')
            self.notification.add_error('type must be a valid CastMemberType: actor or director')

        if self.notification.has_errors:
            raise ValueError(self.notification.messages)
    def __str__(self):
        return f"{self.name} - {self.type}"
    
    def __repr__(self) -> str:
        return f"CastMember(name={self.name}, type={self.type})"
    
    
    def update_cast_member(self, name: str, type: CastMemberType):
        self.name = name
        self.type = type
        self.validate()