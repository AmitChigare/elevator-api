from rest_framework.decorators import action
from .elevator_controller import ElevatorController
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from .models import Elevator
from .serializers import ElevatorSerializer


# Create your views here.
class ElevatorViewSet(viewsets.ModelViewSet):
    queryset = Elevator.objects.all()
    serializer_class = ElevatorSerializer

    @action(detail=True, methods=["post"])
    def start(self, request, pk=None):
        try:
            elevator = self.get_object()
            elevator.status = "running"
            elevator.save()
            return Response(
                {"message": f"Elevator {pk} has started running."}, status=HTTP_200_OK
            )
        except Elevator.DoesNotExist:
            return Response(
                {"error": "Elevator not found."}, status=HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=["post"])
    def stop(self, request, pk=None):
        try:
            elevator = self.get_object()
            ElevatorController.stop_elevator(elevator)
            return Response(
                {"message": f"Elevator {pk} has been stopped."}, status=HTTP_200_OK
            )
        except Elevator.DoesNotExist:
            return Response(
                {"error": "Elevator not found."}, status=HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=["post"])
    def move_to_floor(self, request, pk=None):
        try:
            target_floor = request.data.get("target_floor")
            if target_floor is None or not isinstance(target_floor, int):
                return Response(
                    {"error": "Invalid target_floor provided."},
                    status=HTTP_400_BAD_REQUEST,
                )

            elevator = self.get_object()
            elevator.door_open = False  # Close the door before moving
            elevator.save()

            # Simulating the elevator movement
            if target_floor > elevator.current_floor:
                elevator.direction = "up"
                while elevator.current_floor < target_floor:
                    elevator.current_floor += 1
                    # time.sleep(1)  # Simulating the elevator moving floors
            else:
                elevator.direction = "down"
                while elevator.current_floor > target_floor:
                    elevator.current_floor -= 1
                    # time.sleep(1)  # Simulating the elevator moving floors

            elevator.door_open = True  # Open the door after reaching the target floor
            elevator.save()

            return Response(
                {
                    "message": f"Elevator {pk} has arrived at floor {target_floor}. Door is open."
                },
                status=HTTP_200_OK,
            )
        except Elevator.DoesNotExist:
            return Response(
                {"error": "Elevator not found."}, status=HTTP_400_BAD_REQUEST
            )

    # ... previous viewset code ...
