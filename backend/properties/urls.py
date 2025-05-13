from rest_framework.routers import DefaultRouter
from django.urls import path, include
from rest_framework import routers
from .views import PropertyViewSet, ListedPropertyViewSet, UserProfileViewSet

router = routers.DefaultRouter()
router.register(r'properties', PropertyViewSet)
router.register(r'listed-properties', ListedPropertyViewSet)
router.register(r'user-profiles', UserProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
