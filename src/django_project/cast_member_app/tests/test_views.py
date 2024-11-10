import pytest
from django.test import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.cast_member.domain.cast_member import CastMember, CastMemberType
from core.cast_member.domain.cast_member_repository import CastMemberRepository
from django_project.cast_member_app.repository import DjangoORMCastMemberRepository


@pytest.fixture
def actor() -> CastMember:
    return CastMember(
        name="Tarantino",
        type=CastMemberType.ACTOR
    )


@pytest.fixture
def director() -> CastMember:
    return CastMember(
        name="Quentin Tarantino",
        type=CastMemberType.DIRECTOR
    )


@pytest.fixture
def cast_member_repository() -> CastMemberRepository:
    return DjangoORMCastMemberRepository()


@pytest.mark.django_db
class TestListAPI:
    def test_list(
        self,
        actor: CastMember,
        director: CastMember,
        cast_member_repository: CastMemberRepository
    ):
        actor_id = cast_member_repository.save(actor)
        director_id = cast_member_repository.save(director)

        url = "/api/cast-members/"
        response = APIClient().get(url)
        
        expected_data = {
            "data": [
                {
                    "id": str(actor.id),
                    "name": "Tarantino",
                    "type": "ACTOR"
                },
                {
                    "id": str(director.id),
                    "name": "Quentin Tarantino",
                    "type": "DIRECTOR"
                }
            ]
        }
        

        assert response.status_code == status.HTTP_200_OK # type: ignore
        assert response.data == expected_data # type: ignore
        
        
@pytest.mark.django_db
class TestCreateAPI:
    def test_create_with_valid_data(
        self,
        cast_member_repository: CastMemberRepository
    ):
        url = "/api/cast-members/"
        data = {
            "name": "Tarantino",
            "type": "ACTOR"
        }
        
        response = APIClient().post(url, data=data)
        
        assert response.status_code == status.HTTP_201_CREATED # type: ignore
        assert isinstance(response.data["id"], str) # type: ignore
        
        saved_cast_member = cast_member_repository.get_by_id(response.data["id"]) # type: ignore
        assert saved_cast_member.name == "Tarantino" # type: ignore
        
    def test_when_request_data_with_invalid_data_then_return_400(self):
        url = "/api/cast-members/"
        data = {
            "name": "",
            "type": ""
        }
        
        response = APIClient().post(url, data=data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST # type: ignore