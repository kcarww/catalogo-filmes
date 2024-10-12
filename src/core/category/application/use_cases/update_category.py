from dataclasses import dataclass
from uuid import UUID

from core.category.application.category_repository import CategoryRepository


@dataclass
class UpdateCategoryRequest:
    id: UUID
    name: str | None = None
    description: str | None = None
    is_active: bool | None = None


class UpdateCategory:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def execute(self, request: UpdateCategoryRequest) -> None:
        category = self.repository.get_by_id(request.id)

        current_name = category.name  # type: ignore
        current_description = category.description  # type: ignore

        if request.name is not None:
            current_name = request.name  # type: ignore
        if request.description is not None:
            current_description = request.description  # type: ignore

        if request.is_active is not None:
            if request.is_active:
                category.activate()  # type: ignore

            if not request.is_active:
                category.deactivate()  # type: ignore

        category.update_category(  # type: ignore
            name=current_name, description=current_description
        )

        self.repository.update(category)  # type: ignore
