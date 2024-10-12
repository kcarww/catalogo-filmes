from dataclasses import dataclass
from typing import List
from uuid import UUID

from core.category.application.category_repository import CategoryRepository


@dataclass
class ListCategoryRequest: ...


@dataclass
class ListCategoryOutput:
    id: UUID
    name: str
    description: str
    is_active: bool


@dataclass
class ListCategoryResponse:
    data: List[ListCategoryOutput]


class ListCategory:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def execute(self, request: ListCategoryRequest) -> ListCategoryResponse:
        categories = self.repository.list()
        return ListCategoryResponse(
            data=[
                ListCategoryOutput(
                    id=category.id,
                    name=category.name,
                    description=category.description,
                    is_active=category.is_active,
                )
                for category in categories
            ]
        )
