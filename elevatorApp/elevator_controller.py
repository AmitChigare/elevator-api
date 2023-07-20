from .models import Elevator


class ElevatorController:
    @staticmethod
    def move_elevator(elevator, target_floor):
        if target_floor == elevator.current_floor:
            return
        if target_floor > elevator.current_floor:
            elevator.direction = "up"
            elevator.current_floor += 1
        else:
            elevator.direction = "down"
            elevator.current_floor -= 1
        elevator.save()

    @staticmethod
    def stop_elevator(elevator):
        elevator.direction = "idle"
        elevator.save()
