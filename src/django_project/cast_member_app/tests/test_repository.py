import pytest

from core.cast_member.domain.cast_member import CastMember, CastMemberType
from django_project.cast_member_app.repository import DjangoORMCastMemberRepository
from django_project.cast_member_app.models import CastMember as CastMemberModel

@pytest.mark.django_db
class TestSave:
    def test_saves_cast_member_in_database(self):
        cast_member = CastMember(
            name="Tarantino",
            type=CastMemberType.DIRECTOR
        )
        repository = DjangoORMCastMemberRepository()
        assert CastMemberModel.objects.count() == 0
        repository.save(cast_member)
        assert CastMemberModel.objects.count() == 1
        saved_cast_member = CastMemberModel.objects.get()
        assert saved_cast_member.name == "Tarantino"
        assert saved_cast_member.type == CastMemberType.DIRECTOR
        assert saved_cast_member.id == cast_member.id
    
@pytest.mark.django_db    
class TestGetById:
    def test_returns_cast_member_from_database(self):
        cast_member = CastMemberModel.objects.create(
            name="Tarantino",
            type=CastMemberType.DIRECTOR
        )
        repository = DjangoORMCastMemberRepository()
        retrieved_cast_member = repository.get_by_id(cast_member.id)
        assert retrieved_cast_member.id == cast_member.id # type: ignore
        assert retrieved_cast_member.name == "Tarantino" # type: ignore
        assert retrieved_cast_member.type == CastMemberType.DIRECTOR # type: ignore
        
@pytest.mark.django_db
class TestList:
    def test_returns_all_cast_members_from_database(self):
        cast_member1 = CastMemberModel.objects.create(
            name="Tarantino",
            type=CastMemberType.DIRECTOR
        )
        cast_member2 = CastMemberModel.objects.create(
            name="DiCaprio",
            type=CastMemberType.ACTOR
        )
        repository = DjangoORMCastMemberRepository()
        cast_members = repository.list()
        assert len(cast_members) == 2
        assert cast_members[0].id == cast_member1.id
        
@pytest.mark.django_db
class TestDelete:
    def test_deletes_cast_member_from_database(self):
        cast_member = CastMemberModel.objects.create(
            name="Tarantino",
            type=CastMemberType.DIRECTOR
        )
        repository = DjangoORMCastMemberRepository()
        assert CastMemberModel.objects.count() == 1
        repository.delete(cast_member.id)
        assert CastMemberModel.objects.count() == 0
        
@pytest.mark.django_db
class TestUpdate:
    def test_updates_cast_member_in_database(self):
        cast_member = CastMemberModel.objects.create(
            name="Tarantino",
            type=CastMemberType.DIRECTOR
        )
        repository = DjangoORMCastMemberRepository()
        updated_cast_member = CastMember(
            id=cast_member.id,
            name="Quentin Tarantino",
            type=CastMemberType.DIRECTOR
        )
        repository.update(updated_cast_member)
        cast_member.refresh_from_db()
        assert cast_member.name == "Quentin Tarantino"
        assert cast_member.type == CastMemberType.DIRECTOR