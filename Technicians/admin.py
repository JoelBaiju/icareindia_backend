from django.contrib import admin
from .models import TechnicianProfile,Schedule,TechniciansEarnings


admin.site.register([TechnicianProfile,Schedule,TechniciansEarnings])

