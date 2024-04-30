from django.urls import path, include
from .views import MortyViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'morties', MortyViewSet, basename='morties')

urlpatterns = [
    path('', include(router.urls)),
]
