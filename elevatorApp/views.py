from rest_framework.decorators import action
from .elevator_controller import ElevatorController
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from .models import Elevator, ElevatorRequest
from .serializers import ElevatorSerializer, ElevatorRequestSerializer
import time


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


class ElevatorRequestView(APIView):
    def post(self, request, elevator_id):
        try:
            floor = request.data.get("floor")
            if floor is None or not isinstance(floor, int):
                return Response(
                    {"error": "Invalid floor provided."}, status=HTTP_400_BAD_REQUEST
                )

            elevator = Elevator.objects.get(pk=elevator_id)
            current_floor = elevator.current_floor

            if current_floor == floor:
                elevator.door_open = True
                return Response(
                    {"message": f"Elevator on current floor. Opening the Doors..."},
                    status=HTTP_200_OK,
                )

            elevator_request = ElevatorRequest(elevator=elevator, floor=floor)
            elevator_request.save()
            elevator.current_floor = floor

            # Closing the door if the door is open
            if elevator.door_open:
                elevator.door_open = False
            # Start the elevator if its not already running
            if elevator.status != "running":
                elevator.status = "running"

            elevator.save()
            return Response(
                {
                    "message": f"Request added to Elevator {elevator_id} queue. Current on floor: {current_floor}"
                },
                status=HTTP_201_CREATED,
            )
        except Elevator.DoesNotExist:
            return Response(
                {"error": "Elevator not found."}, status=HTTP_400_BAD_REQUEST
            )


class ElevatorMaintenanceView(APIView):
    def post(self, request, elevator_id):
        try:
            elevator = Elevator.objects.get(pk=elevator_id)
            elevator.operational = False
            elevator.save()
            return Response(
                {"message": f"Elevator {elevator_id} is now under maintenance."},
                status=HTTP_200_OK,
            )
        except Elevator.DoesNotExist:
            return Response(
                {"error": "Elevator not found."}, status=HTTP_400_BAD_REQUEST
            )


class ElevatorDoorOpenView(APIView):
    def post(self, request, elevator_id):
        try:
            elevator = Elevator.objects.get(pk=elevator_id)
            elevator.door_open = True
            elevator.save()
            return Response(
                {"message": f"The door of Elevator {elevator_id} is now open."},
                status=HTTP_200_OK,
            )
        except Elevator.DoesNotExist:
            return Response(
                {"error": "Elevator not found."}, status=HTTP_400_BAD_REQUEST
            )


class ElevatorDoorCloseView(APIView):
    def post(self, request, elevator_id):
        try:
            elevator = Elevator.objects.get(pk=elevator_id)
            elevator.door_open = False
            elevator.save()
            return Response(
                {"message": f"The door of Elevator {elevator_id} is now closed."},
                status=HTTP_200_OK,
            )
        except Elevator.DoesNotExist:
            return Response(
                {"error": "Elevator not found."}, status=HTTP_400_BAD_REQUEST
            )
