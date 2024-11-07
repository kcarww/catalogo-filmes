from enum import StrEnum
from dataclasses import field, dataclass
import uuid
from uuid import UUID

class CastMemberType(StrEnum):
    DIRECTOR = 'DIRECTOR'
    ACTOR = 'ACTOR'
    
    
@dataclass
class CastMember:
    name: str
    type: CastMemberType
    id: UUID = field(default_factory=uuid.uuid4)
    
    def __post_init__(self):
        self.validate()
    
    def validate(self):
        if len(self.name) > 255:
            raise ValueError('name cannot be longer than 255')
        
        if not self.name:
            raise ValueError('name cannot be empty')
        
        if not self.type in CastMemberType:
            raise ValueError('type must be a valid CastMemberType: actor or director')
        
    def __str__(self):
        return f"{self.name} - {self.type}"
    
    def __repr__(self) -> str:
        return f"CastMember(name={self.name}, type={self.type})"
    
    def __eq__(self, other):
        if not isinstance(other, CastMember):
            return False
        return self.id == other.id
    
    def update_cast_member(self, name, type):
        self.name = name
        self.type = type
        self.validate()