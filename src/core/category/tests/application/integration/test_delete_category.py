from core.category.application.use_cases.delete_category import (
    DeleteCategory,
    DeleteCategoryRequest,
)
from core.category.domain.category import Category
from core.category.infra.in_memory_category_repository import InMemoryCategoryRepository


class TestDeleteCategory:
    def test_delete_category_from_repository(self):
        category = Category(name="Movie")
        repository = InMemoryCategoryRepository(categories=[category])
        use_case = DeleteCategory(repository)

        request = DeleteCategoryRequest(id=category.id)
        response = use_case.execute(request)
        assert response is None
