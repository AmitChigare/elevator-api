from django.db import models

# Create your models here.


class Elevator(models.Model):
    current_floor = models.PositiveIntegerField(default=1)
    direction = models.CharField(max_length=5, default="up")  # "up", "down", or "idle"
    status = models.CharField(
        max_length=10, default="idle"
    )  # "idle", "running", or "maintenance"
    operational = models.BooleanField(default=True)
    door_open = models.BooleanField(default=False)

    def __str__(self):
        return f"Elevator {self.id}"


class ElevatorRequest(models.Model):
    elevator = models.ForeignKey(Elevator, on_delete=models.CASCADE)
    floor = models.PositiveIntegerField()
    disabled = models.BooleanField(default=False)

    def __str__(self):
        return f"Elevator {self.elevator_id} - Floor {self.floor}"
