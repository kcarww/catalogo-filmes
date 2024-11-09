from unittest.mock import create_autospec
import pytest

from core.cast_member.application.use_cases.list_cast_member_use_case import CastMemberOutput, ListCastMemberOutput, ListCastMemberRequest, ListCastMemberUseCase
from core.cast_member.domain.cast_member import CastMember, CastMemberType
from core.cast_member.domain.cast_member_repository import CastMemberRepository
from core.cast_member.infra.in_memory_cast_member_repository import InMemoryCastMemberRepository


class TestListCastMember:
    @pytest.fixture
    def actor(self) -> CastMember:
        return CastMember(
            name="Tarantino actor",
            type=CastMemberType.ACTOR
        )

    @pytest.fixture
    def director(self) -> CastMember:
        return CastMember(
            name="Tarantino director",
            type=CastMemberType.DIRECTOR
        )

    def test_when_no_test_member_then_return_empty_list(self):
        use_case = ListCastMemberUseCase(InMemoryCastMemberRepository())
        response = use_case.execute(request=ListCastMemberRequest())
        assert response == ListCastMemberOutput(data=[])

    def test_when_populated_repository_then_return_list_of_cast_members(
        self,
        actor: CastMember,
        director: CastMember
    ):
        use_case = ListCastMemberUseCase(InMemoryCastMemberRepository(
            cast_members=[actor, director]
        ))
        response = use_case.execute(request=ListCastMemberRequest())
        assert response == ListCastMemberOutput(data=[
            CastMemberOutput(
                id=actor.id,
                name=actor.name,
                type=actor.type
            ),
            CastMemberOutput(
                id=director.id,
                name=director.name,
                type=director.type
            )
        ])
