from rest_framework import serializers
from ..models import Animal, AnimalCategory, Breed
from users.serializers import UserSerializer

class BreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Breed
        fields = ('id', 'name')

class AnimalCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalCategory
        fields = ('id', 'name')

class AnimalListSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    breed = serializers.StringRelatedField()
    
    class Meta:
        model = Animal
        fields = ('id', 'name', 'category', 'breed', 'age', 'price', 'image_url', 'is_sold')

class AnimalDetailSerializer(serializers.ModelSerializer):
    category = AnimalCategorySerializer(read_only=True)
    breed = BreedSerializer(read_only=True)
    farmer = UserSerializer(read_only=True)

    class Meta:
        model = Animal
        fields = '__all__'