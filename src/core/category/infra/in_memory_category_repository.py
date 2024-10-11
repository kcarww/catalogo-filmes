from dataclasses import dataclass, field

from src.core.category.application.category_repository import CategoryRepository


@dataclass
class InMemoryCategoryRepository(CategoryRepository):
    categories: list = field(default_factory=list)
    
    def save(self, category):
        self.categories.append(category)