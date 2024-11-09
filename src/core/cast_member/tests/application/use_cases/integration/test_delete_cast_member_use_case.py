

from core.cast_member.application.use_cases.delete_cast_member import DeleteCastMember, DeleteCastMemberRequest
from core.cast_member.domain.cast_member import CastMember, CastMemberType
from core.cast_member.infra.in_memory_cast_member_repository import InMemoryCastMemberRepository


class TestDeleteCastMember:
    def test_delete_cast_member_from_repository(self):
        cast_member = CastMember(
            name="Tarantino",
            type=CastMemberType.DIRECTOR
        )
        
        repository = InMemoryCastMemberRepository(
            cast_members=[cast_member]
        )
        use_case = DeleteCastMember(repository)
        
        
        assert repository.get_by_id(cast_member.id) is not None
        use_case.execute(DeleteCastMemberRequest(id=cast_member.id))
        assert repository.get_by_id(cast_member.id) is None
        
        