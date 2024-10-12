from unittest.mock import create_autospec
import uuid

import pytest
from core.category.application.category_repository import CategoryRepository
from core.category.application.use_cases.exceptions import CategoryNotFound
from core.category.domain.category import Category
from core.category.application.use_cases.get_category import (
    GetCategory,
    GetCategoryRequest,
    GetCategoryResponse,
)
from core.category.infra.in_memory_category_repository import InMemoryCategoryRepository


class TestGetCategory:
    def test_get_category_by_id(self):
        category = Category(name="movie")
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case = GetCategory(repository=mock_repository)
        request = GetCategoryRequest(id=category.id)

        response = use_case.execute(request)

        assert response == GetCategoryResponse(
            id=category.id, name="movie", description="", is_active=True
        )

    def test_when_category_does_not_exists_then_raise_exception(self):
        category_movie = Category(name="movie")
        repository = InMemoryCategoryRepository(categories=[category_movie])
        use_case = GetCategory(repository=repository)
        request = GetCategoryRequest(id=uuid.uuid4())

        with pytest.raises(CategoryNotFound) as assert_error:
            category_id = use_case.execute(request)
