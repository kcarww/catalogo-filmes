from unittest.mock import create_autospec
import uuid
import pytest

from core.category.domain.category import Category
from core.category.domain.category_repository import CategoryRepository
from core.genre.application.exceptions import InvalidGenre, RelatedCategoriesNotFound
from core.genre.application.use_cases.create_genre import CreateGenre
from core.genre.domain.genre import Genre
from core.genre.domain.genre_repository import GenreRepository


@pytest.fixture
def mock_genre_repository() -> GenreRepository:
    return create_autospec(GenreRepository)


@pytest.fixture
def movie_category() -> Category:
    return Category(name="Movie")


@pytest.fixture
def documentary_category() -> Category:
    return Category(name="Documentary")


@pytest.fixture
def mock_category_repository_with_categories(movie_category, documentary_category) -> CategoryRepository:
    repository = create_autospec(CategoryRepository)
    repository.list.return_value = [movie_category, documentary_category]
    return repository


@pytest.fixture
def mock_empty_category_repository() -> CategoryRepository:
    repository = create_autospec(CategoryRepository)
    repository.list.return_value = []
    return repository


class TestCreateGenre:
    def test_when_categories_do_not_exist_then_raise_related_categories_not_found(
        self, mock_empty_category_repository, mock_genre_repository
    ):
        use_case = CreateGenre(
            repository=mock_genre_repository,
            category_repository=mock_empty_category_repository
        )
        category_id = uuid.uuid4()
        input = CreateGenre.Input(name="Action", categories={category_id})
        with pytest.raises(RelatedCategoriesNotFound) as exc_info:
            use_case.execute(input)
        assert str(category_id) in str(exc_info.value)

    def test_when_created_genre_is_invalid_then_raise_invalid_genre(
        self,
        movie_category,
        mock_category_repository_with_categories,
        mock_genre_repository
    ):
        use_case = CreateGenre(
            repository=mock_genre_repository,
            category_repository=mock_category_repository_with_categories
        )

        input = CreateGenre.Input(
            name="",
            categories={movie_category.id}
        )

        with pytest.raises(InvalidGenre) as exc_info:
            use_case.execute(input)
        assert "name is required" in str(exc_info.value)

    def test_when_created_genre_is_valid_and_categories_exists_then_create_genre(
        self,
        movie_category,
        documentary_category,
        mock_category_repository_with_categories,
        mock_genre_repository
    ):
        use_case = CreateGenre(
            repository=mock_genre_repository,
            category_repository=mock_category_repository_with_categories
        )
        input = CreateGenre.Input(
            name="Action",
            categories={movie_category.id, documentary_category.id}
        )
        output = use_case.execute(input)
        assert output.id is not None
        mock_genre_repository.save.assert_called_once_with(
            Genre(
                id=output.id,
                name="Action",
                is_active=True,
                categories={movie_category.id, documentary_category.id}
            )
        )

    def test_create_genre_without_categories(
        self,
        mock_category_repository_with_categories,
        mock_genre_repository
    ):
        use_case = CreateGenre(
            repository=mock_genre_repository,
            category_repository=mock_category_repository_with_categories
        )
        input = CreateGenre.Input(
            name="Action",
            categories=set()
        )
        output = use_case.execute(input)
        assert output.id is not None
        mock_genre_repository.save.assert_called_once_with(
            Genre(
                id=output.id,
                name="Action",
                is_active=True,
                categories=set()
            )
        )
