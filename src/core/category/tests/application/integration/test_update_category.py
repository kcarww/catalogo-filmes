from abc import update_abstractmethods
from core.category.application.use_cases.update_category import UpdateCategory, UpdateCategoryRequest
from core.category.domain.category import Category
from core.category.infra.in_memory_category_repository import InMemoryCategoryRepository


class TestUpdateCategory:
    def test_can_update_category_name_and_description(self):
        category_movie = Category(name='movie')
        repository = InMemoryCategoryRepository(categories=[category_movie])
        use_case = UpdateCategory(repository=repository)
        request = UpdateCategoryRequest(
            id=category_movie.id,
            name='new name',
            description='new description'
        )

        use_case.execute(request)
        update_category = repository.get_by_id(category_movie.id)
        assert update_category.name == 'new name'
        assert update_category.description == 'new description'
        