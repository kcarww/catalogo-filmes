import uuid
import pytest
from uuid import UUID

from core.genre.domain.genre import Genre


class TestGenre:
    def test_name_is_required(self):

        with pytest.raises(
            TypeError, match="missing 1 required positional argument: 'name'"
        ):
            Genre()

    def test_cannot_create_genre_with_empty_name(self):
        with pytest.raises(ValueError, match="name is required"):
            Genre(name="")

    def test_name_must_have_less_than_255_characters(self):
        with pytest.raises(ValueError, match="name must have less than 256 characters"):
            Genre(name="a" * 266)

    def test_genre_must_be_created_with_id_as_uuid(self):
        genre = Genre(name="movie")
        assert isinstance(genre.id, UUID)

    def test_created_genre_with_default_values(self):
        genre = Genre(name="movie")
        assert genre.name == "movie"
        assert genre.is_active is True

    def test_genre_is_created_as_active_by_default(self):
        genre = Genre(name="movie")
        assert genre.is_active is True


class TestUpdateGenre:
    def test_update_genre_with_name_and_description(self):
        genre = Genre(name="filme")

        genre.change_name(name="serie")

        assert genre.name == "serie"

    def test_update_genre_with_invalid_name_raises_exception(self):
        genre = Genre(name="a")
        with pytest.raises(ValueError, match="name must have less than 256 characters"):
            genre.change_name(name="1" * 256)


class TestActivate:

    def test_activate_genre(self):
        genre = Genre(name="filme", is_active=False)

        genre.activate()

        assert genre.is_active is True

    def test_deactivate_genre(self):
        genre = Genre(name="filme", is_active=True)

        genre.deactivate()

        assert genre.is_active is False


class TestEquality:
    def test_when_genres_have_same_id_they_are_equal(self):
        common_id = uuid.uuid4()
        genre1 = Genre(name="filme", id=common_id)
        genre2 = Genre(name="filme", id=common_id)

        assert genre1 == genre2
