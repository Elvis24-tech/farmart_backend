from rest_framework import viewsets
from ..models import AnimalCategory, Breed
from ..serializers.animal_serializers import AnimalCategorySerializer, BreedSerializer

class AnimalCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AnimalCategory.objects.all()
    serializer_class = AnimalCategorySerializer

class BreedViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer