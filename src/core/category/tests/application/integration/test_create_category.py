from core.category.application.use_cases.create_category import (
    CreateCategory,
    CreateCategoryRequest,
    CreateCategoryResponse,
)
from core.category.infra.in_memory_category_repository import InMemoryCategoryRepository


class TestCreateCategory:
    def test_create_category_with_valid_date(self):
        repository = InMemoryCategoryRepository()
        use_case = CreateCategory(repository=repository)
        request = CreateCategoryRequest(
            name="movie", description="movie", is_active=True
        )

        category_id = use_case.execute(request)

        assert category_id is not None
        assert isinstance(category_id, CreateCategoryResponse)
        assert len(repository.categories) == 1
        saved_category = repository.categories[0]
        assert saved_category.name == "movie"
        assert saved_category.description == "movie"
        assert saved_category.is_active is True

    # def test_create_category_with_invalid_data(self):
    #     use_case = CreateCategory(repository=MagicMock(InMemoryCategoryRepository))
    #     with pytest.raises(InvalidCategoryData, match="name is required") as assert_error:
    #         request = CreateCategoryRequest(
    #         name="",
    #         description="movie",
    #         is_active=True
    #     )
    #         use_case.execute(request)

    #     assert assert_error.type == InvalidCategoryData
    #     assert str(assert_error.value) == "name is required"
