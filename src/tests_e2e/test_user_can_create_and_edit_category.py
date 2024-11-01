
import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.mark.django_db
class TestCreateAndEditCategory:
    def test_user_can_create_and_edit_category(self, api_client: APIClient):
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

        edit_response = api_client.put(
            f"/api/categories/{created_category_id}/",
            {
                "name": "Documentary",
                "description": "Documentary description",
                "is_active": True,
            },
            format="json"
        )
        assert edit_response.status_code == 204
        list_response = api_client.get('/api/categories/')
        assert list_response.data == {
            "data": [
                {
                    "id": created_category_id,
                    "name": "Documentary",
                    "description": "Documentary description",
                    "is_active": True,
                }
            ]
        }
