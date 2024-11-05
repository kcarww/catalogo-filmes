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