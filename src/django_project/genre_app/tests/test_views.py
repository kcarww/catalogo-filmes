import uuid
import pytest

from rest_framework import status
from rest_framework.test import APIClient
from django.test import override_settings
from django.urls import reverse

from core.category.domain.category import Category
from core.genre.domain.genre import Genre
from django_project.category_app.repository import DjangoORMCategoryRepository
from django_project.genre_app.repository import DjangoORMGenreRepository


@pytest.fixture
def category_movie():
    return Category(
        name="Movie",
        description="Movie description",
    )


@pytest.fixture
def category_documentary():
    return Category(
        name="Documentary",
        description="Documentary description",
    )


@pytest.fixture
def category_repository() -> DjangoORMCategoryRepository:
    return DjangoORMCategoryRepository()


@pytest.fixture
def genre_romance(category_movie: Category, category_documentary: Category) -> Genre:
    return Genre(
        name="Romance",
        is_active=True,
        categories={category_movie.id, category_documentary.id},
    )


@pytest.fixture
def genre_drama() -> Genre:
    return Genre(
        name="Drama",
        is_active=True,
        categories=set(),
    )


@pytest.fixture
def genre_repository() -> DjangoORMGenreRepository:
    return DjangoORMGenreRepository()

@pytest.mark.django_db
class TestListAPI:
    def test_list_genres_and_categories(
        self,
        category_movie: Category,
        category_documentary: Category,
        category_repository: DjangoORMCategoryRepository,
        genre_romance: Genre,
        genre_drama: Genre,
        genre_repository: DjangoORMGenreRepository,
    ) -> None:
        category_repository.save(category_movie)
        category_repository.save(category_documentary)
        genre_repository.save(genre_romance)
        genre_repository.save(genre_drama)

        url = "/api/genres/"
        response = APIClient().get(url)
        
        assert response.status_code == status.HTTP_200_OK # type: ignore
        assert response.data["data"] # type: ignore
        assert response.data["data"][0]["id"] == str(genre_romance.id) # type: ignore
        assert response.data["data"][0]["name"] == "Romance" # type: ignore
        assert response.data["data"][0]["is_active"] is True # type: ignore
        assert set(response.data["data"][0]["categories"]) == { # type: ignore
            str(category_documentary.id),
            str(category_movie.id),
        }
        assert response.data["data"][1]["id"] == str(genre_drama.id) # type: ignore
        assert response.data["data"][1]["name"] == "Drama" # type: ignore
        assert response.data["data"][1]["is_active"] is True # type: ignore
        assert response.data["data"][1]["categories"] == [] # type: ignore
        
        
@pytest.mark.django_db
class TestCreateAPI:
    def test_when_request_data_is_valid_then_create_genre(
        self,
        category_repository: DjangoORMCategoryRepository,
        category_movie: Category,
        genre_repository: DjangoORMGenreRepository,
    ) -> None:
        category_repository.save(category_movie)

        url = "/api/genres/"
        data = {
            "name": "Romance",
            "categories": [category_movie.id],
        }
        response = APIClient().post(url, data=data)

        assert response.status_code == status.HTTP_201_CREATED # type: ignore
        assert response.data["id"] # type: ignore

        saved_genre = genre_repository.get_by_id(response.data["id"]) # type: ignore
        assert saved_genre == Genre(
            id=uuid.UUID(response.data["id"]), # type: ignore
            name="Romance",
            is_active=True,
            categories={category_movie.id},
        )

    def test_when_request_data_is_invalid_then_return_400(self) -> None:
        url = "/api/genres/"
        data = {
            "name": "",
        }
        response = APIClient().post(url, data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST # type: ignore
        assert response.data == {"name": ["This field may not be blank."]} # type: ignore

    def test_when_related_categories_do_not_exist_then_return_400(
        self,
    ) -> None:
        url = "/api/genres/"
        data = {
            "name": "Romance",
            "categories": [uuid.uuid4()],
        }
        response = APIClient().post(url, data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST # type: ignore
        assert "Categories with provided IDs not found" in response.data["error"] # type: ignore
        
        
    
    
@pytest.mark.django_db
class TestDeleteAPI:
    def test_when_genre_pk_is_invalid_then_return_400(self) -> None:
        url = "/api/genres/invalid_uuid/"
        response = APIClient().delete(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST # type: ignore
        assert response.data == {"id": ["Must be a valid UUID."]} # type: ignore

    def test_when_genre_not_found_then_return_404(self) -> None:
        url = f"/api/genres/{str(uuid.uuid4())}/"
        response = APIClient().delete(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND # type: ignore

    def test_when_genre_found_then_delete_genre(
        self,
        category_repository: DjangoORMCategoryRepository,
        category_movie: Category,
        category_documentary: Category,
        genre_repository: DjangoORMGenreRepository,
        genre_romance: Genre,
    ) -> None:
        category_repository.save(category_movie)
        category_repository.save(category_documentary)
        genre_repository.save(genre_romance)

        url = f"/api/genres/{str(genre_romance.id)}/"
        response = APIClient().delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT # type: ignore
        assert genre_repository.get_by_id(genre_romance.id) is None
        
@pytest.mark.django_db
class TestUpdateAPI:
    def test_when_request_data_is_valid_then_update_genre(
        self,
        category_repository: DjangoORMCategoryRepository,
        category_movie: Category,
        category_documentary: Category,
        genre_repository: DjangoORMGenreRepository,
        genre_romance: Genre,
    ) -> None:
        category_repository.save(category_movie)
        category_repository.save(category_documentary)
        genre_repository.save(genre_romance)

        url = f"/api/genres/{str(genre_romance.id)}/"
        data = {
            "name": "Drama",
            "is_active": True,
            "categories": [category_documentary.id],
        }
        response = APIClient().put(url, data=data, format='json')

        assert response.status_code == status.HTTP_204_NO_CONTENT # type: ignore
        updated_genre = genre_repository.get_by_id(genre_romance.id)
        assert updated_genre.name == "Drama" # type: ignore
        assert updated_genre.is_active is True # type: ignore
        assert updated_genre.categories == {category_documentary.id} # type: ignore

    def test_when_request_data_is_invalid_then_return_400(
        self,
        genre_drama: Genre,
    ) -> None:
        url = f"/api/genres/{str(genre_drama.id)}/"
        data = {
            "name": "",
            "is_active": True,
            "categories": [],
        }
        response = APIClient().put(url, data=data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST # type: ignore
        assert response.data == {"name": ["This field may not be blank."]} # type: ignore

    def test_when_related_categories_do_not_exist_then_return_400(
        self,
        category_repository: DjangoORMCategoryRepository,
        category_movie: Category,
        category_documentary: Category,
        genre_repository: DjangoORMGenreRepository,
        genre_romance: Genre,
    ) -> None:
        category_repository.save(category_movie)
        category_repository.save(category_documentary)
        genre_repository.save(genre_romance)

        url = f"/api/genres/{str(genre_romance.id)}/"
        data = {
            "name": "Romance",
            "is_active": True,
            "categories": [uuid.uuid4()],  # non-existent category
        }
        response = APIClient().put(url, data=data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST # type: ignore
        # assert "Categories with provided IDs not found" in response.data["error"] # type: ignore

    def test_when_genre_does_not_exist_then_return_404(self) -> None:
        url = f"/api/genres/{str(uuid.uuid4())}/"
        data = {
            "name": "Romance",
            "is_active": True,
            "categories": [],
        }
        response = APIClient().put(url, data=data, format='json')

        assert response.status_code == status.HTTP_404_NOT_FOUND # type: ignore
