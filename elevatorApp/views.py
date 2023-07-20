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

    def get_next_destination_floor(self, elevator):
        """
        Get the next destination floor for the given elevator based on user requests.
        """
        # Fetch all pending requests for the elevator
        pending_requests = ElevatorRequest.objects.filter(elevator=elevator).order_by(
            "floor"
        )

        if not pending_requests:
            return None

        # Get the next destination floor based on the elevator's current direction
        if elevator.direction == "up":
            next_floor = min(pending_requests, key=lambda req: req.floor).floor
        elif elevator.direction == "down":
            next_floor = max(pending_requests, key=lambda req: req.floor).floor
        else:
            # If the elevator is idle, set the next floor to the closest floor in any direction
            up_floors = [
                req.floor
                for req in pending_requests
                if req.floor >= elevator.current_floor
            ]
            down_floors = [
                req.floor
                for req in pending_requests
                if req.floor <= elevator.current_floor
            ]

            if up_floors and down_floors:
                next_floor = min(
                    up_floors + down_floors,
                    key=lambda floor: abs(elevator.current_floor - floor),
                )
            elif up_floors:
                next_floor = min(up_floors)
            elif down_floors:
                next_floor = max(down_floors)
            else:
                return None

        return next_floor

    def save_user_request(self, elevator_id, floor):
        """
        Save user request to the list of requests for the given elevator.
        """
        try:
            elevator = Elevator.objects.get(pk=elevator_id)
            elevator_request = ElevatorRequest(elevator=elevator, floor=floor)
            if elevator_request.DoesNotExist:
                elevator.create(elevator=elevator, floor=floor)
            else:
                elevator_request.save()
        except Elevator.DoesNotExist:
            pass

    #######################OLD FUNCTIONS################
    @action(detail=True, methods=["post"])
    def call_elevator(self, request, pk=None):
        try:
            elevator = self.get_object()
            if not elevator.operational:
                return Response(
                    {
                        "message": "Elevator is under maintenance. Cannot process request."
                    },
                    status=HTTP_200_OK,
                )

            floor = request.data.get("floor")
            if floor is None or not isinstance(floor, int):
                return Response(
                    {"error": "Invalid floor provided."}, status=HTTP_400_BAD_REQUEST
                )

            if elevator.current_floor == floor:
                return Response(
                    {"message": "Elevator on the same floor, Opening the door..."},
                    status=HTTP_200_OK,
                )

            if elevator.door_open:
                # Close the door before moving to the floor
                elevator.door_open = False
                elevator.save()

            # Start the elevator if it's not already running
            if elevator.status != "running":
                elevator.status = "running"
                elevator.save()

            # Check if there are any pending requests
            next_floor = self.get_next_destination_floor(elevator)

            if next_floor is not None:
                # Elevator is already running, add the new floor to the pending requests
                self.save_user_request(pk, floor)
                return Response(
                    {
                        "message": f"Elevator {pk} has a pending request. The next destination floor is {next_floor}."
                    },
                    status=HTTP_200_OK,
                )
            else:
                # Elevator is idle, move directly to the requested floor
                # Simulate the elevator movement
                if floor > elevator.current_floor:
                    elevator.direction = "up"
                    while elevator.current_floor < floor:
                        elevator.current_floor += 1
                        time.sleep(1)  # Simulating the elevator moving floors
                else:
                    elevator.direction = "down"
                    while elevator.current_floor > floor:
                        elevator.current_floor -= 1
                        time.sleep(1)  # Simulating the elevator moving floors

                # Create a new ElevatorRequest for the current floor
                self.save_user_request(pk, elevator.current_floor)

                # Open the door after reaching the target floor
                elevator.door_open = True
                elevator.save()

                # Stop the elevator
                elevator.status = "idle"
                elevator.save()

                return Response(
                    {
                        "message": f"Elevator {pk} has arrived at floor {floor}. Door is open. Elevator is stopped."
                    },
                    status=HTTP_200_OK,
                )

        except Elevator.DoesNotExist:
            return Response(
                {"error": "Elevator not found."}, status=HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=["get"])
    def get_pending_requests(self, request, pk=None):
        try:
            elevator = Elevator.objects.get(pk=pk)
            pending_requests = ElevatorRequest.objects.filter(
                elevator=elevator
            ).order_by("floor")
            serializer = ElevatorRequestSerializer(pending_requests, many=True)
            return Response(serializer.data, status=HTTP_200_OK)
        except Elevator.DoesNotExist:
            return Response(
                {"error": "Elevator not found."}, status=HTTP_400_BAD_REQUEST
            )


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Elevator, ElevatorRequest
from .serializers import ElevatorSerializer


class ElevatorRequestView(APIView):
    def post(self, request, elevator_id):
        try:
            elevator = Elevator.objects.get(pk=elevator_id)
            if not elevator.operational:
                return Response(
                    {
                        "message": "Elevator is under maintenance. Cannot process request."
                    },
                    status=status.HTTP_200_OK,
                )

            floor = request.data.get("floor")
            if floor is None or not isinstance(floor, int):
                return Response(
                    {"error": "Invalid floor provided."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            current_floor = elevator.current_floor

            if current_floor == floor:
                elevator.door_open = True
                elevator.save()
                return Response(
                    {"message": f"Elevator on current floor. Opening the Doors..."},
                    status=status.HTTP_200_OK,
                )

            # Start the elevator if it's not already running
            if elevator.status != "running":
                elevator.status = "running"
                elevator.save()

            # Check if there are any pending requests
            pending_requests = ElevatorRequest.objects.filter(
                elevator=elevator, disabled=False
            ).order_by("floor")
            if pending_requests:
                next_floor = pending_requests[0].floor

                while True:
                    # Move the elevator towards the next floor
                    if elevator.direction == "up":
                        elevator.current_floor += 1
                    else:
                        elevator.current_floor -= 1
                    elevator.save()

                    # Simulate the elevator moving floors
                    time.sleep(1)

                    # Check if the elevator has reached the next floor
                    if elevator.current_floor == next_floor:
                        # Open the door at the destination floor
                        elevator.door_open = True
                        elevator.save()

                        # Disable the current pending request
                        pending_requests[0].disabled = True
                        pending_requests[0].save()

                        # Close the door after a short delay (simulating user interaction)
                        time.sleep(2)
                        elevator.door_open = False
                        elevator.save()

                        # Remove the completed request from the pending requests
                        pending_requests = ElevatorRequest.objects.filter(
                            elevator=elevator, disabled=False
                        ).order_by("floor")

                        # If there are no more pending requests, stop the elevator
                        if not pending_requests:
                            elevator.status = "idle"
                            elevator.save()
                            break

                        # Otherwise, update the next destination floor
                        next_floor = pending_requests[0].floor

                        # Continue to the next iteration to move towards the new destination floor

                return Response(
                    {
                        "message": f"Elevator {elevator_id} has arrived at floor {next_floor}. Door is open. Elevator is stopped."
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                # Elevator is idle, move directly to the requested floor
                # Simulate the elevator movement
                if floor > elevator.current_floor:
                    elevator.direction = "up"
                    while elevator.current_floor < floor:
                        elevator.current_floor += 1
                        elevator.save()
                        time.sleep(1)  # Simulating the elevator moving floors
                else:
                    elevator.direction = "down"
                    while elevator.current_floor > floor:
                        elevator.current_floor -= 1
                        elevator.save()
                        time.sleep(1)  # Simulating the elevator moving floors

                # Create a new ElevatorRequest for the current floor
                elevator_request = ElevatorRequest(
                    elevator=elevator, floor=elevator.current_floor
                )
                elevator_request.save()

                # Open the door after reaching the target floor
                elevator.door_open = True
                elevator.save()

                # Stop the elevator if there are no more pending requests
                elevator.status = "idle"
                elevator.save()

                return Response(
                    {
                        "message": f"Elevator {elevator_id} has arrived at floor {floor}. Door is open. Elevator is stopped."
                    },
                    status=status.HTTP_200_OK,
                )

            # Elevator has reached the desired floor, update the next floor properly
            next_floor = None
            pending_requests = ElevatorRequest.objects.filter(
                elevator=elevator, disabled=False
            ).order_by("floor")
            if pending_requests:
                next_floor = pending_requests[0].floor

            return Response(
                {
                    "message": f"Elevator {elevator_id} has arrived at floor {current_floor}. Door is open. Elevator is stopped.",
                    "next_floor": next_floor,
                },
                status=status.HTTP_200_OK,
            )

        except Elevator.DoesNotExist:
            return Response(
                {"error": "Elevator not found."}, status=status.HTTP_400_BAD_REQUEST
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
