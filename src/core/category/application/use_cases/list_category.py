from abc import ABC
from dataclasses import dataclass, field
from typing import Generic, List, TypeVar
from uuid import UUID

from core.category.domain.category_repository import CategoryRepository
import config

@dataclass
class ListCategoryRequest: 
    order_by: str = "name"
    current_page: int = 1


@dataclass
class ListCategoryOutput:
    id: UUID
    name: str
    description: str
    is_active: bool

@dataclass
class ListOutputMeta:
    current_page: int = 1
    per_page: int = config.DEFAULT_PAGINATION_SIZE 
    total: int = 0
    
T = TypeVar("T")

@dataclass
class ListCategoryResponse(Generic[T], ABC):
    data: List[T]
    meta: ListOutputMeta = field(default_factory=ListOutputMeta)


class ListCategory:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def execute(self, request: ListCategoryRequest) -> ListCategoryResponse:
        categories = self.repository.list()
        sorted_categories = sorted([
                ListCategoryOutput(
                    id=category.id,
                    name=category.name,
                    description=category.description,
                    is_active=category.is_active,
                )
                for category in categories
            ], key=lambda category: getattr(category, request.order_by))
        
        page_offset = (request.current_page - 1) * config.DEFAULT_PAGINATION_SIZE
        categories_page = sorted_categories[page_offset:page_offset + config.DEFAULT_PAGINATION_SIZE]
        
        return ListCategoryResponse(
            data=categories_page,
            meta=ListOutputMeta(
                current_page=request.current_page,
                per_page=config.DEFAULT_PAGINATION_SIZE,
                total=len(sorted_categories)
            )
        )
