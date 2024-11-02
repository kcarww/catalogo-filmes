from unittest.mock import create_autospec
import uuid
import pytest

from core.category.domain.category import Category
from core.category.domain.category_repository import CategoryRepository
from core.category.infra.in_memory_category_repository import InMemoryCategoryRepository
from core.genre.application.exceptions import InvalidGenre, RelatedCategoriesNotFound
from core.genre.application.use_cases.create_genre import CreateGenre
from core.genre.domain.genre import Genre
from core.genre.infra.in_memory_genre_repository import InMemoryGenreRepository


@pytest.fixture
def movie_category() -> Category:
    return Category(name="Movie")


@pytest.fixture
def documentary_category() -> Category:
    return Category(name="Documentary")


@pytest.fixture
def category_repository(movie_category: Category, documentary_category: Category) -> CategoryRepository:
    return InMemoryCategoryRepository(
        categories=[movie_category, documentary_category]
    )


class TestCreateGenre:
    def test_create_genre_with_associated_categories(
        self,
        movie_category: Category,
        documentary_category: Category,
        category_repository: CategoryRepository,
    ):
        genre_repository = InMemoryGenreRepository()
        use_case = CreateGenre(
            repository=genre_repository,
            category_repository=category_repository,
        )
        input = CreateGenre.Input(
            name="Action",
            category_ids={movie_category.id, documentary_category.id},
        )
        
        output = use_case.execute(input)
        assert output.id is not None
        saved_genre = genre_repository.get_by_id(output.id)
        assert saved_genre.name == "Action" # type: ignore
        assert saved_genre.is_active is True # type: ignore
        assert len(saved_genre.categories) == 2 # type: ignore
        
    def test_when_categories_do_not_exist_then_raise_related_categories_not_found(
        self,
        category_repository
        ):
        genre_repository = InMemoryGenreRepository()
        use_case = CreateGenre(
            repository=genre_repository,
            category_repository=category_repository
        )
        input = CreateGenre.Input(
            name="Action",
            category_ids={uuid.uuid4()}
        )
        with pytest.raises(RelatedCategoriesNotFound) as exc_info:
            use_case.execute(input)