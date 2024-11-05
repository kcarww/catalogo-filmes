import uuid
import pytest

from core.category.domain.category import Category
from core.genre.domain.genre import Genre
from django_project.category_app.repository import DjangoORMCategoryRepository
from django_project.genre_app.models import Genre as GenreORM
from django_project.genre_app.repository import DjangoORMGenreRepository


@pytest.mark.django_db
class TestSave:
    def test_saves_genre_in_database(self):
        genre = Genre(name="Action")
        repository = DjangoORMGenreRepository()
        assert GenreORM.objects.count() == 0
        repository.save(genre)
        assert GenreORM.objects.count() == 1
        
        saved_genre = GenreORM.objects.get()
        assert saved_genre.id == genre.id
        assert saved_genre.name == genre.name
        assert saved_genre.is_active == genre.is_active
        
        
    def test_saves_genre_with_related_categories_in_database(self):
        repository = DjangoORMGenreRepository()
        category_repository = DjangoORMCategoryRepository()
        
        category = Category(name="Movie")
        category_repository.save(category)
        
        genre = Genre(name="Action")
        genre.add_category(category.id)
        
        assert GenreORM.objects.count() == 0
        repository.save(genre)
        assert GenreORM.objects.count() == 1
        
        saved_genre = GenreORM.objects.get()
        assert saved_genre.categories.count() == 1
        
        related_category = saved_genre.categories.get()
        assert related_category.id == category.id

@pytest.mark.django_db      
class TestFind:
    def test_returns_genre_by_id(self):
        genre = Genre(name="Action")
        repository = DjangoORMGenreRepository()
        repository.save(genre)
        
        found_genre = repository.get_by_id(genre.id)
        assert found_genre.id == genre.id # type: ignore
        assert found_genre.name == genre.name # type: ignore
        assert found_genre.is_active == genre.is_active # type: ignore
        
    def test_returns_none_when_genre_does_not_exist(self):
        repository = DjangoORMGenreRepository()
        assert repository.get_by_id(uuid.uuid4()) is None
        
@pytest.mark.django_db
class TestDelete:
    def test_deletes_genre(self):
        genre = Genre(name="Action")
        repository = DjangoORMGenreRepository()
        repository.save(genre)
        
        assert GenreORM.objects.count() == 1
        repository.delete(genre.id)
        assert GenreORM.objects.count() == 0
    def test_delete_genre_with_id_that_does_not_exist(self):
        repository = DjangoORMGenreRepository()
        assert repository.delete(uuid.uuid4()) is None
        
@pytest.mark.django_db
class TestList:
    def test_returns_list_of_genres(self):
        genre1 = Genre(name="Action")
        genre2 = Genre(name="Adventure")
        repository = DjangoORMGenreRepository()
        repository.save(genre1)
        repository.save(genre2)
        
        genres = repository.list()
        assert len(genres) == 2
        
        assert genre1 in genres
        assert genre2 in genres
        
    def test_returns_empty_list_when_no_genres(self):
        repository = DjangoORMGenreRepository()
        assert repository.list() == []
        
@pytest.mark.django_db
class TestUpdate:
    def test_updates_genre(self):
        genre = Genre(name="Action")
        repository = DjangoORMGenreRepository()
        repository.save(genre)
        
        updated_genre = Genre(id=genre.id, name="Adventure")
        repository.update(updated_genre)
        
        found_genre = repository.get_by_id(genre.id)
        assert found_genre.name == "Adventure" # type: ignore
        
    def test_update_genre_with_id_that_does_not_exist(self):
        genre = Genre(id=uuid.uuid4(), name="Action")
        repository = DjangoORMGenreRepository()
        assert repository.update(genre) is None