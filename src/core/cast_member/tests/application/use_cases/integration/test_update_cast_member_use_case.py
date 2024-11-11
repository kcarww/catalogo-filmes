from unittest.mock import create_autospec
import uuid

import pytest

from core.cast_member.application.use_cases.exceptions import CastMemberNotFound, InvalidCastMember
from core.cast_member.application.use_cases.update_cast_member_use_case import UpdateCastMember, UpdateCastMemberRequest
from core.cast_member.domain.cast_member import CastMember, CastMemberType
from core.cast_member.domain.cast_member_repository import CastMemberRepository
from core.cast_member.infra.in_memory_cast_member_repository import InMemoryCastMemberRepository


class TestUpdateCastMember:
    @pytest.fixture
    def actor(self) -> CastMember:
        return CastMember(
            name="Tarantino",
            type=CastMemberType.DIRECTOR
        )
    
    def test_update_cast_member_name_and_type(
        self,
        actor: CastMember,
        ):
        use_case = UpdateCastMember(InMemoryCastMemberRepository(
            cast_members=[actor]
        ))
        use_case.execute(
            UpdateCastMemberRequest(
                id=actor.id,
                name="Quentin Tarantino",
                type=CastMemberType.ACTOR
            )
        )
        
        assert actor.name == "Quentin Tarantino"
        assert actor.type == CastMemberType.ACTOR
        
    def test_when_cast_member_not_found(self):
        use_case = UpdateCastMember(InMemoryCastMemberRepository())
        request = UpdateCastMemberRequest(
                    id=uuid.uuid4(),
                    name="Quentin Tarantino",
                    type=CastMemberType.ACTOR
                )
        with pytest.raises(CastMemberNotFound) as exc:
            use_case.execute(request)
        assert str(exc.value) == f"Cast member with id {request.id} not found"
        
    def test_when_cast_member_is_updated_to_invalid_state_then_raise_exception(
        self,
        actor: CastMember,
    ) -> None:
        use_case = UpdateCastMember(InMemoryCastMemberRepository(
            cast_members=[actor]
        ))
        request = UpdateCastMemberRequest(
            id=actor.id,
            name="",
            type=""
        )
        with pytest.raises(InvalidCastMember) as exc:
            use_case.execute(request)
        assert "name cannot be empty" in str(exc.value)