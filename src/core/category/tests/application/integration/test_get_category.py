import uuid

import pytest
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
        category_movie = Category(name="movie")
        repository = InMemoryCategoryRepository(categories=[category_movie])
        use_case = GetCategory(repository=repository)
        request = GetCategoryRequest(id=category_movie.id)

        category_id = use_case.execute(request)

        assert category_id is not None
        assert isinstance(category_id, GetCategoryResponse)
        assert category_id.id == category_movie.id
        assert category_id.name == category_movie.name
        assert category_id.description == category_movie.description
        assert category_id.is_active == category_movie.is_active

    def test_when_category_does_not_exists_then_raise_exception(self):
        category_movie = Category(name="movie")
        repository = InMemoryCategoryRepository(categories=[category_movie])
        use_case = GetCategory(repository=repository)
        request = GetCategoryRequest(id=uuid.uuid4())

        with pytest.raises(CategoryNotFound) as assert_error:
            category_id = use_case.execute(request)
