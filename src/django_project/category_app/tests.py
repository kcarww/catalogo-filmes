from django.test import TestCase
from rest_framework.test import APITestCase


class TestCategoryAPI(APITestCase):
    def test_list_categories(self):
        url = '/api/categories/'
        response = self.client.get(url)
        expected_data = [
            {
                "id": "a5b518c3-a34a-459a-b33f-c986e1f62114",
                "name": "Movie",
                "description": "Movies category",
                "is_active": True
            },
            {
                "id": "18836c68-c71d-4346-b545-37f6205f09c9",
                "name": "Movie 2",
                "description": "Movies category",
                "is_active": False
            }
        ]
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_data)