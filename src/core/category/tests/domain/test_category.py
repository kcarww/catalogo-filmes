import uuid
import pytest
from uuid import UUID

from core.category.domain.category import Category
import core.category.domain.category as category


class TestCategory:
    def test_name_is_required(self):

        with pytest.raises(
            TypeError, match="missing 1 required positional argument: 'name'"
        ):
            Category()

    def test_cannot_create_category_with_empty_name(self):
        with pytest.raises(ValueError, match="name is required"):
            Category(name="")

    def test_name_must_have_less_than_255_characters(self):
        with pytest.raises(ValueError, match="name must have less than 256 characters"):
            Category(name="a" * 266)

    def test_category_must_be_created_with_id_as_uuid(self):
        category = Category(name="movie")
        assert isinstance(category.id, UUID)

    def test_created_category_with_default_values(self):
        category = Category(name="movie")
        assert category.name == "movie"
        assert category.description == ""
        assert category.is_active is True

    def test_category_is_created_as_active_by_default(self):
        category = Category(name="movie")
        assert category.is_active is True


class TestUpdateCategory:
    def test_update_category_with_name_and_description(self):
        category = Category(name="filme", description="filmes em geral")

        category.update_category(name="serie", description="series em geral")

        assert category.name == "serie"
        assert category.description == "series em geral"

    def test_update_category_with_invalid_name_raises_exception(self):
        category = Category(name="a", description="filmes em geral")
        with pytest.raises(ValueError, match="name must have less than 256 characters"):
            category.update_category(name="1" * 256, description="whatever")

    def test_cannot_update_category_with_empty_name(self):
        category = Category(name="a", description="filmes em geral")
        with pytest.raises(ValueError, match="name is required"):
            category.update_category(name="", description="whatever")


class TestActivate:

    def test_activate_category(self):
        category = Category(name="filme", is_active=False)

        category.activate()

        assert category.is_active is True

    def test_deactivate_category(self):
        category = Category(name="filme", is_active=True)

        category.deactivate()

        assert category.is_active is False


class TestEquality:
    def test_when_categories_have_same_id_they_are_equal(self):
        common_id = uuid.uuid4()
        category1 = Category(name="filme", id=common_id)
        category2 = Category(name="filme", id=common_id)

        assert category1 == category2
