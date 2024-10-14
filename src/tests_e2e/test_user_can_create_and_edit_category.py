
import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestCreateAndEditCategory:
    def test_user_can_create_and_edit_category(self):
        api_client = APIClient()
        list_response = api_client.get('/api/categories/')
        assert list_response.data == {"data": []}

        create_response = api_client.post(
            '/api/categories/',
            data={
                "name": "Test Category",
                "description": "description"
            })

        assert create_response.status_code == 201
        created_category_id = create_response.data["id"]

        list_response = api_client.get("/api/categories/")
        assert list_response.data == {
            "data": [
                {
                    "id": created_category_id,
                    "name": "Test Category",
                    "description": "description",
                    "is_active": True
                }
            ]
        }

        update_request = api_client.put(
            f'/api/categories/{created_category_id}/',
            data={
                "name": "edited",
                "description": "edited",
                "is_active": False
            }
        )
        assert update_request.status_code == 204
        list_response = api_client.get('/api/categories/')
        assert list_response.data == {
            "data": [
                {
                    "id": created_category_id,
                    "name": "edited",
                    "description": "edited",
                    "is_active": False
                }
            ]
        }
