from uuid import UUID
import pytest
from src.core.category.application.create_category import InvalidCategoryData, create_category


class TestCreateCategory:
    def test_create_category_with_valid_date(self):
        category_id = create_category(
            name="movie",
            description="movie",
            is_active=True
        )
        
        assert category_id is not None
        assert isinstance(category_id, UUID)
        
    def test_create_category_with_invalid_data(self):
        with pytest.raises(InvalidCategoryData, match="name is required") as assert_error:
            create_category(name="")

        assert_error.type == InvalidCategoryData
        assert_error.value == "name is required"

