from unittest.mock import create_autospec
import uuid

import pytest

from core.cast_member.application.use_cases.exceptions import CastMemberNotFound, InvalidCastMember
from core.cast_member.application.use_cases.update_cast_member_use_case import UpdateCastMember, UpdateCastMemberRequest
from core.cast_member.domain.cast_member import CastMember, CastMemberType
from core.cast_member.domain.cast_member_repository import CastMemberRepository


class TestUpdateCastMember:
    @pytest.fixture
    def actor(self) -> CastMember:
        return CastMember(
            name="Tarantino",
            type=CastMemberType.DIRECTOR
        )
        
    @pytest.fixture
    def mock_repository(self, actor: CastMember) -> CastMemberRepository:
        repository = create_autospec(CastMemberRepository)
        repository.get_by_id.return_value = actor
        return repository
    
    def test_update_cast_member_name_and_type(
        self,
        actor: CastMember,
        mock_repository: CastMemberRepository
        ):
        use_case = UpdateCastMember(mock_repository)
        use_case.execute(
            UpdateCastMemberRequest(
                id=actor.id,
                name="Quentin Tarantino",
                type=CastMemberType.ACTOR
            )
        )
        
        assert actor.name == "Quentin Tarantino"
        assert actor.type == CastMemberType.ACTOR
        mock_repository.update.assert_called_once_with(actor)
        
    def test_when_cast_member_not_found(self):
        mock_repository = create_autospec(CastMemberRepository)
        mock_repository.get_by_id.return_value = None
        use_case = UpdateCastMember(mock_repository)
        request = UpdateCastMemberRequest(
                    id=uuid.uuid4(),
                    name="Quentin Tarantino",
                    type=CastMemberType.ACTOR
                )
        with pytest.raises(CastMemberNotFound) as exc:
            use_case.execute(request)
        mock_repository.update.assert_not_called()
        assert str(exc.value) == f"Cast member with id {request.id} not found"
        
    def test_when_cast_member_is_updated_to_invalid_state_then_raise_exception(
        self,
        mock_repository: CastMemberRepository,
        actor: CastMember,
    ) -> None:
        use_case = UpdateCastMember(mock_repository)
        request = UpdateCastMemberRequest(
            id=actor.id,
            name="",
            type=""
        )
        with pytest.raises(InvalidCastMember) as exc:
            use_case.execute(request)
        mock_repository.update.assert_not_called()
        assert "name cannot be empty" in str(exc.value)