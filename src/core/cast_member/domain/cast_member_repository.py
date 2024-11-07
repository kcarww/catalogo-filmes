from abc import ABC, abstractmethod
from uuid import UUID

from core.cast_member.domain.cast_member import CastMember

class CastMemberRepository(ABC):
    @abstractmethod
    def save(self, cast_member: CastMember):
        raise NotImplementedError
    
    @abstractmethod
    def get_by_id(self, id: UUID) -> CastMember | None:
        raise NotImplementedError
    
    @abstractmethod
    def delete(self, id: UUID):
        raise NotImplementedError
    
    @abstractmethod
    def list(self) -> list[CastMember]:
        raise NotImplementedError
    
    def update(self, cast_member: CastMember):
        raise NotImplementedError