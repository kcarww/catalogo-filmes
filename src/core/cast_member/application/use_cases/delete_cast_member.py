from dataclasses import dataclass
from uuid import UUID

from core.cast_member.application.use_cases.exceptions import CastMemberNotFound
from core.cast_member.domain.cast_member_repository import CastMemberRepository


@dataclass
class DeleteCastMemberRequest:
    id: UUID
    
class DeleteCastMember:
    def __init__(self, repository: CastMemberRepository):
        self.repository = repository
        
    def execute(self, request: DeleteCastMemberRequest):
        cast_member = self.repository.get_by_id(request.id)

        if cast_member is None:
            raise CastMemberNotFound(f"CastMember with {request.id} not found")
        
        self.repository.delete(cast_member.id)
        
