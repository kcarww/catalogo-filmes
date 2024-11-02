from dataclasses import dataclass
from uuid import UUID

from core.category.domain.category_repository import CategoryRepository
from core.genre.application.exceptions import GenreNotFound, RelatedCategoriesNotFound
from core.genre.domain.genre_repository import GenreRepository


@dataclass(kw_only=True)
class UpdateGenre:
    repository: GenreRepository
    category_repository: CategoryRepository
    
    @dataclass
    class Input:
        id: UUID
        name: str
        is_active: bool
        categories: set[UUID]
        
    def execute(self, input: Input) -> None:
        genre = self.repository.get_by_id(input.id)
        
        if genre is None:
            raise GenreNotFound(f"Genre with id {input.id} not found")
        
        category_ids = {category.id for category in self.category_repository.list()}
        if not input.categories.issubset(category_ids):
            raise RelatedCategoriesNotFound(
                f"Categories with ids {input.categories - category_ids} not found"
            )
        try:
            if input.is_active:
                genre.activate()
            if input.is_active is False:
                genre.deactivate()
            genre.change_name(input.name)
            
            genre.update_categories(input.categories)
        except ValueError as error:
            raise ValueError(str(error)) from error
        
        self.repository.update(genre)
    