from rest_framework.test import APITestCase

from core.category.domain.category import Category
from django_project.category_app.repository import DjangoORMCategoryRepository


class TestCategoryAPI(APITestCase):
    def test_list_categories(self):
        category_movie = Category(
            name="Movie",
            description="Movies category",
            is_active=True
        )
        repository = DjangoORMCategoryRepository()
        repository.save(category_movie)
        
        url = '/api/categories/'
        response = self.client.get(url)
        expected_data = [
            {
                "id": str(category_movie.id),
                "name": category_movie.name,
                "description": category_movie.description,
                "is_active": category_movie.is_active
            }
        ]
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_data)