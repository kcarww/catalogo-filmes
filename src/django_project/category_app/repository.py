from uuid import UUID
from core.category.domain.category import Category
from core.category.domain.category_repository import CategoryRepository
from django_project.category_app.models import Category as CategoryModel


class DjangoORMCategoryRepository(CategoryRepository):
    def __init__(self, category_model: CategoryModel = CategoryModel): # type: ignore
        self.category_model = category_model
        
    
    def save(self, category: Category) -> None:
        category_orm = CategoryModelMapper.to_model(category)
        category_orm.save()
        # self.category_model.objects.create(
        #     id=category.id,
        #     name=category.name,
        #     description=category.description,
        #     is_active=category.is_active
        # )
        
    def get_by_id(self, id: UUID) -> Category | None:
        try:
            category = CategoryModelMapper.to_entity(self.category_model.objects.get(id=id))
            return category
        except self.category_model.DoesNotExist:
            return None
        
    def delete(self, id: UUID) -> None:
        self.category_model.objects.filter(id=id).delete()
        
    def list(self) -> list[Category]:
        return [
            CategoryModelMapper.to_entity(category)
            for category in self.category_model.objects.all()
        ]
        
    def update(self, category: Category) -> None:
        self.category_model.objects.filter(id=category.id)\
            .update(
                name=category.name,
                description=category.description,
                is_active=category.is_active
            )
            
class CategoryModelMapper:
    @staticmethod
    def to_model(category: Category) -> CategoryModel:
        return CategoryModel(
            id=category.id,
            name=category.name,
            description=category.description,
            is_active=category.is_active
        )
        
    @staticmethod
    def to_entity(category: CategoryModel) -> Category:
        return Category(
            id=category.id,
            name=category.name,
            description=category.description,
            is_active=category.is_active
        )