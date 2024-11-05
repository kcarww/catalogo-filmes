from dataclasses import dataclass, field
from uuid import UUID
from core.category.domain.category_repository import CategoryRepository
from core.genre.application.exceptions import InvalidGenre, RelatedCategoriesNotFound
from core.genre.domain.genre import Genre
from core.genre.domain.genre_repository import GenreRepository


class CreateGenre:
    def __init__(self, repository: GenreRepository, category_repository: CategoryRepository):
        self.repository = repository
        self.category_repository = category_repository

    @dataclass
    class Input:
        name: str
        categories: set[UUID] = field(default_factory=set)
        is_active: bool = True

    @dataclass
    class Output:
        id: UUID

    def execute(self, input: Input) -> Output:
        print(input.categories, '<--------')
        category_ids = {
            category.id for category in self.category_repository.list()}
        if not input.categories.issubset(category_ids):
            raise RelatedCategoriesNotFound(
                f"Categories with provided IDs not found: {input.categories - category_ids}")

        try:
            genre = Genre(
                name=input.name,
                is_active=input.is_active,
                categories=input.categories
            )
        except ValueError as e:
            raise InvalidGenre(str(e)) from e

        self.repository.save(genre)
        return self.Output(id=genre.id)
