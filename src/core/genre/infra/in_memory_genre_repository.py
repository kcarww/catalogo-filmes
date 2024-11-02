# pylint: disable=unnecessary-comprehension
from dataclasses import dataclass, field
from uuid import UUID

from core.genre.domain.genre_repository import GenreRepository
from core.genre.domain.genre import Genre


@dataclass
class InMemoryGenreRepository(GenreRepository):
    genres: list = field(default_factory=list)  # pylint: disable = E0601

    def save(self, genre):
        self.genres.append(genre)

    def get_by_id(self, id: UUID) -> Genre | None:
        for genre in self.genres:
            if genre.id == id:
                return genre
        return None

    def delete(self, id: UUID) -> None:
        genre = self.get_by_id(id)
        self.genres.remove(genre)

    def update(self, genre: Genre) -> None:
        old_genre = self.get_by_id(genre.id)
        if old_genre:
            self.genres.remove(old_genre)
            self.genres.append(genre)

    def list(self) -> list[Genre]:
        return [genre for genre in self.genres]
