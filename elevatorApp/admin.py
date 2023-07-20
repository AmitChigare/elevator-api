from django.contrib import admin
from .models import Elevator, ElevatorRequest

# Register your models here.
admin.site.register(Elevator)
admin.site.register(ElevatorRequest)
