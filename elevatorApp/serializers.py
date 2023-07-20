from rest_framework import serializers
from .models import Elevator, ElevatorRequest


class ElevatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Elevator
        fields = "__all__"
