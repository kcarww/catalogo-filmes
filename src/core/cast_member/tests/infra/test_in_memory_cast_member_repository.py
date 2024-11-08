import uuid

from core.cast_member.domain.cast_member import CastMember, CastMemberType
from core.cast_member.infra.in_memory_cast_member_repository import InMemoryCastMemberRepository


class TestSave:
    def test_can_save_cast_member(self):
        repository = InMemoryCastMemberRepository()
        cast_member = CastMember(
            name = "Any Name",
            type=CastMemberType.ACTOR
        )
        repository.save(cast_member)
        
        assert len(repository.cast_members) == 1
        assert repository.get_by_id(cast_member.id) == cast_member
        
class TestGetById:
    def test_can_get_cast_member_by_id(self):
        director = CastMember(
            name='Tarantino',
            type=CastMemberType.DIRECTOR
        )
        
        repository = InMemoryCastMemberRepository(
            cast_members=[director]
        )
        
        cast_member = repository.get_by_id(director.id)
        assert cast_member == director
        
class TestList:
    def test_can_list_all_cast_members(self):
        director = CastMember(
            name='Tarantino',
            type=CastMemberType.DIRECTOR
        )
        
        actor = CastMember(
            name='DiCaprio',
            type=CastMemberType.ACTOR
        )
        
        repository = InMemoryCastMemberRepository(
            cast_members=[director, actor]
        )
        
        cast_members = repository.list()
        assert len(cast_members) == 2
        assert director in cast_members
        assert actor in cast_members
        
class TestUpdate:
    def test_can_update_cast_member(self):
        director = CastMember(
            name='Tarantino',
            type=CastMemberType.DIRECTOR
        )
        
        repository = InMemoryCastMemberRepository(
            cast_members=[director]
        )
        
        director.name = 'Quentin Tarantino'
        repository.update(director)
        
        assert len(repository.cast_members) == 1
        assert repository.get_by_id(director.id).name == 'Quentin Tarantino' # type: ignore
        
class TestDelete:
    def test_can_delete_cast_member(self):
        director = CastMember(
            name='Tarantino',
            type=CastMemberType.DIRECTOR
        )
        
        repository = InMemoryCastMemberRepository(
            cast_members=[director]
        )
        
        repository.delete(director.id)
        
        assert len(repository.cast_members) == 0
        assert repository.get_by_id(director.id) is None