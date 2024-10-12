from unittest.mock import create_autospec
import uuid

from core.category.application.category_repository import CategoryRepository
from core.category.application.use_cases.update_category import (
    UpdateCategory,
    UpdateCategoryRequest,
)
from core.category.domain.category import Category


class TestUpdateCategory:
    def test_update_category_name(self):
        category = Category(
            id=uuid.uuid4(),
            name="Filme",
            description="Categoria para filmes",
            is_active=True,
        )

        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case = UpdateCategory(repository=mock_repository)
        request = UpdateCategoryRequest(id=category.id, name="Série")
        response = use_case.execute(request)

        assert category.name == "Série"
        mock_repository.update.assert_called_once_with(category)

    def test_update_category_description(self):
        category = Category(
            id=uuid.uuid4(),
            name="Filme",
            description="Categoria para filmes",
            is_active=True,
        )

        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case = UpdateCategory(repository=mock_repository)
        request = UpdateCategoryRequest(
            id=category.id, description="Descrição da série"
        )
        use_case.execute(request)

        assert category.description == "Descrição da série"
        mock_repository.update.assert_called_once_with(category)

    def test_can_deactivate_category(self):
        category = Category(
            id=uuid.uuid4(),
            name="Filme",
            description="Categoria para filmes",
            is_active=True,
        )

        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case = UpdateCategory(repository=mock_repository)
        request = UpdateCategoryRequest(id=category.id, is_active=False)
        use_case.execute(request)

        assert not category.is_active
        mock_repository.update.assert_called_once_with(category)

    def test_can_activate_category(self):
        category = Category(
            id=uuid.uuid4(),
            name="Filme",
            description="Categoria para filmes",
            is_active=False,
        )

        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case = UpdateCategory(repository=mock_repository)
        request = UpdateCategoryRequest(id=category.id, is_active=True)
        use_case.execute(request)

        assert category.is_active
        mock_repository.update.assert_called_once_with(category)
