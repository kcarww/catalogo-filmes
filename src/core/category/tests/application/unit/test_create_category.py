from unittest.mock import MagicMock
import pytest
from src.core.category.application.exceptions import InvalidCategoryData
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository
from src.core.category.application.create_category import CreateCategory, CreateCategoryRequest, CreateCategoryResponse


class TestCreateCategory:
    def test_create_category_with_valid_date(self):
        mock_repository = MagicMock(InMemoryCategoryRepository)
        use_case = CreateCategory(repository=mock_repository)
        request = CreateCategoryRequest(
            name="movie",
            description="movie",
            is_active=True
        )

        category_id = use_case.execute(request)

        assert category_id is not None
        assert isinstance(category_id, CreateCategoryResponse)
        assert mock_repository.save.called

    def test_create_category_with_invalid_data(self):
        use_case = CreateCategory(repository=MagicMock(InMemoryCategoryRepository))
        with pytest.raises(InvalidCategoryData, match="name is required") as assert_error:
            request = CreateCategoryRequest(
            name="",
            description="movie",
            is_active=True
        )
            use_case.execute(request)

        assert assert_error.type == InvalidCategoryData
        assert str(assert_error.value) == "name is required"
