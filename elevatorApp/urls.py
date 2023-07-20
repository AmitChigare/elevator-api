from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ElevatorViewSet,
)

router = DefaultRouter()
router.register(r"elevators", ElevatorViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
