from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ElevatorViewSet,
    ElevatorRequestView,
    ElevatorMaintenanceView,
    ElevatorDoorOpenView,
    ElevatorDoorCloseView,
)

router = DefaultRouter()
router.register(r"elevators", ElevatorViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("elevators/<int:elevator_id>/request/", ElevatorRequestView.as_view()),
    path("elevators/<int:elevator_id>/maintenance/", ElevatorMaintenanceView.as_view()),
    path("elevators/<int:elevator_id>/door/open/", ElevatorDoorOpenView.as_view()),
    path("elevators/<int:elevator_id>/door/close/", ElevatorDoorCloseView.as_view()),
]
