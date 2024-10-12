# pylint: disable=unnecessary-comprehension
from dataclasses import dataclass, field
from uuid import UUID

from core.category.application.category_repository import CategoryRepository
from core.category.domain.category import Category


@dataclass
class InMemoryCategoryRepository(CategoryRepository):
    categories: list = field(default_factory=list)  # pylint: disable = E0601

    def save(self, category):
        self.categories.append(category)

    def get_by_id(self, id: UUID) -> Category | None:
        for category in self.categories:
            if category.id == id:
                return category
        return None

    def delete(self, id: UUID) -> None:
        category = self.get_by_id(id)
        self.categories.remove(category)

    def update(self, category: Category) -> None:
        old_category = self.get_by_id(category.id)
        if old_category:
            self.categories.remove(old_category)
            self.categories.append(category)

    def list(self) -> list[Category]:
        return [category for category in self.categories]
