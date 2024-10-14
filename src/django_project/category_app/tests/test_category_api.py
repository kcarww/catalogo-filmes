import uuid
import pytest
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from core.category.domain.category import Category
from django_project.category_app.repository import DjangoORMCategoryRepository


@pytest.fixture
def category_movie():
    return Category(
        name="movie",
        description="Movies category",
    )


@pytest.fixture
def category_documentary():
    return Category(
        name="documentary",
        description="Documentary category",
    )


@pytest.fixture
def category_repository() -> DjangoORMCategoryRepository:
    return DjangoORMCategoryRepository()


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
        expected_data = {
            "data": [
                {
                    "id": str(category_movie.id),
                    "name": category_movie.name,
                    "description": category_movie.description,
                    "is_active": category_movie.is_active
                }
            ]
        }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_data)


@pytest.mark.django_db
class TestRetrieveAPI:
    def test_when_id_is_invalid(self):
        url = "/api/categories/invalid_id/"
        response = APIClient().get(url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_return_category_when_exists(
        self,
        category_movie: Category,
        category_documentary: Category,
        category_repository: DjangoORMCategoryRepository
    ) -> None:
        category_repository.save(category_movie)
        category_repository.save(category_documentary)
        url = f"/api/categories/{category_documentary.id}/"
        response = APIClient().get(url)

        expected_data = {
            "data": {
                "id": str(category_documentary.id),
                "name": category_documentary.name,
                "description": category_documentary.description,
                "is_active": category_documentary.is_active
            }
        }

        assert response.status_code == status.HTTP_200_OK
        assert response.data == expected_data

    def test_if_category_does_not_exist(self):
        url = "/api/categories/18836c68-c71d-4346-b545-37f6205f09c9/"
        response = APIClient().get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestCreateCategoryAPI:
    def test_when_payload_is_invalid_then_return_400(self):
        url = "/api/categories/"
        response = APIClient().post(
            url,
            data={
                "name": "",
                "description": "Movies category",
                "is_active": True
            }
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_when_payload_is_valid_then_create_category_and_return_201(
        self,
        category_repository: DjangoORMCategoryRepository
    ):
        url = "/api/categories/"
        response = APIClient().post(
            url,
            data = {
                "name": "Movie",
                "description": "Movies category",
                "is_active": True
            }
        )
        created_category_id = uuid.UUID(response.data["id"])
        assert response.status_code == status.HTTP_201_CREATED
        assert category_repository.get_by_id(created_category_id) == Category(
            id=created_category_id,
            name="Movie",
            description="Movies category",
            is_active=True
        )
