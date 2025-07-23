from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.animal_views import AnimalViewSet
from .views.category_views import AnimalCategoryViewSet, BreedViewSet
from .views.order_views import OrderViewSet

router = DefaultRouter()
router.register(r'animals', AnimalViewSet)
router.register(r'categories', AnimalCategoryViewSet)
router.register(r'breeds', BreedViewSet)
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
]