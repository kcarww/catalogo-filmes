from uuid import UUID

from core.cast_member.infra.in_memory_cast_member_repository import InMemoryCastMemberRepository
from core.cast_member.application.use_cases.create_cast_member import CreateCastMember, CreateCastMemberRequest
from core.cast_member.domain.cast_member import CastMemberType


class TestCreateCastMember:
    def test_can_create_cast_member_with_valid_data(self):
        repository = InMemoryCastMemberRepository()
        use_case = CreateCastMember(repository=repository)
        request = CreateCastMemberRequest(
            name="Tarantino",
            type=CastMemberType.DIRECTOR
        )
        response = use_case.execute(request)
        
        assert response is not None
        assert isinstance(response.id, UUID)
        assert len(repository.cast_members) == 1
        
        cast_member = repository.cast_members[0]
        assert cast_member.id == response.id
        assert cast_member.name == request.name
        assert cast_member.type == request.type
        
    