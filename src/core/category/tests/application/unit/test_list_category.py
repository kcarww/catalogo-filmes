from unittest.mock import create_autospec

from core.category.application.category_repository import CategoryRepository
from core.category.application.use_cases.list_category import ListCategory, ListCategoryOutput, ListCategoryRequest, ListCategoryResponse
from core.category.domain.category import Category


class TestListCategory:
    def test_when_no_categories_in_repository(self):
        category = Category(
            name='movie'
        )
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.list.return_value = []
        use_case = ListCategory(repository=mock_repository)
        request = ListCategoryRequest()
        
        response = use_case.execute(request)
        
        assert response == ListCategoryResponse(
            data=[],
            
        )
        
    def test_when_categories_in_repository(self):
        category = Category(
            name='movie'
        )
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.list.return_value = [category]
        use_case = ListCategory(repository=mock_repository)
        request = ListCategoryRequest()
        
        response = use_case.execute(request)
        
        assert response == ListCategoryResponse(
            data=[
                ListCategoryOutput(
                    id= category.id,
                    name= category.name,
                    description= category.description,
                    is_active= category.is_active
                )
            ]
        )