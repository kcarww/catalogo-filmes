from rest_framework import serializers

from core.video.domain.value_objects import Rating

class VideoRatingField(serializers.ChoiceField):
    def __init__(self, **kwargs):
        choices = [(type.name, type.name) for type in Rating]
        super().__init__(choices=choices, **kwargs)
    
    def to_internal_value(self, data):
        return Rating(super().to_internal_value(data))
    
    def to_representation(self, value):
        return str(super().to_representation(value))
    

class SetField(serializers.ListField):
    
    def to_internal_value(self, data):
        return set(super().to_internal_value(data))
    
    def to_representation(self, data):
        return list(super().to_representation(data))
    
class CreateVideoRequestSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    description = serializers.CharField()
    launch_year = serializers.IntegerField()
    rating = VideoRatingField(required=True)
    duration = serializers.IntegerField()
    categories = SetField(child=serializers.UUIDField(), required=False)
    genres = SetField(child=serializers.UUIDField(), required=False)
    cast_members = SetField(child=serializers.UUIDField(), required=False)
    
class CreateVideoResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    
class VideoResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    title = serializers.CharField()
    description = serializers.CharField()
    launch_year = serializers.IntegerField()
    rating = VideoRatingField()
    duration = serializers.IntegerField()
    categories = SetField(child=serializers.UUIDField())
    genres = SetField(child=serializers.UUIDField())
    cast_members = SetField(child=serializers.UUIDField())
    
class ListVideoResponseSerializer(serializers.Serializer):
    data = VideoResponseSerializer(many=True) # type: ignore