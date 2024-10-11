from core.category.domain.category import Category
from core.category.infra.in_memory_category_repository import InMemoryCategoryRepository


class TestInMemoryCateoryRepository:
    def test_can_save_category(self):
        repository = InMemoryCategoryRepository()
        category = Category(
            name="filme",
            description="some description"
        )
        
        repository.save(category)
        
        assert len(repository.categories) == 1
        assert repository.categories[0] == category