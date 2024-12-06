# yourapp/tasks.py

from celery import shared_task
from django.utils import timezone
from datetime import timedelta, time
from ..Technicians.models import Technician, TimeSlotAvailability

@shared_task
def populate_technician_availability():
    technicians = Technician.objects.all()
    today = timezone.now().date()
    
    # Generate time slots from 8 AM to 7 PM
    time_slots = [time(hour=h) for h in range(8, 20)]

    for technician in technicians:
        for day_offset in range(7):  # Next 7 days
            availability_date = today + timedelta(days=day_offset)
            for time_slot in time_slots:
                try:
                    TimeSlotAvailability.objects.get_or_create(
                        technician=technician,
                        date=availability_date,
                        time_slot=time_slot
                    )
                except Exception as e:
                    # Log or handle the exception as needed
                    print(f"Error creating availability for {technician} on {availability_date} at {time_slot}: {e}")
