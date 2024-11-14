from rest_framework import serializers

class CategoryResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255)
    description = serializers.CharField()
    is_active = serializers.BooleanField()
    

class ListOutputMetaSerializer(serializers.Serializer):
    current_page = serializers.IntegerField()
    per_page = serializers.IntegerField()
    total = serializers.IntegerField()

class ListCategoryResponseSerializer(serializers.Serializer):
    data = CategoryResponseSerializer(many=True) # type: ignore
    meta = ListOutputMetaSerializer()

class RetrieveCategoryRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField()

class RetrieveCategoryResponseSerializer(serializers.Serializer):
    data = CategoryResponseSerializer(source='*') # type: ignore
    
    
class CreateCategoryResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    
class CreateCategoryRequestSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255, allow_blank=False)
    description = serializers.CharField()
    is_active = serializers.BooleanField(default=True)
    

class UpdateCategoryRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=True)
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=True, allow_blank=True, allow_null=False)
    is_active = serializers.BooleanField(required=True)
    
    
    
class DeleteCategoryRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField()