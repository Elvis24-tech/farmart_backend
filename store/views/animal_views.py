from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Animal
from ..serializers.animal_serializers import AnimalListSerializer, AnimalDetailSerializer

class AnimalViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for listing and retrieving animals.
    Supports filtering by category_id, breed_id, and is_sold.
    Supports searching by name, description, and breed name.
    """
    queryset = Animal.objects.filter(is_sold=False).select_related('category', 'breed', 'farmer')
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'breed', 'is_sold']
    search_fields = ['name', 'description', 'breed__name', 'category__name']
    ordering_fields = ['price', 'created_at', 'age']

    def get_serializer_class(self):
        if self.action == 'list':
            return AnimalListSerializer
        return AnimalDetailSerializer