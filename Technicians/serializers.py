from rest_framework import serializers

from .models import TechnicianProfile,Schedule

class TechniciansProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechnicianProfile
        fields = ['name','phone','alt_phone','gender','longitude','lattitude','id']
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return list(representation.values())
    
    
    
class TechnicianImageSerializer(serializers.ModelSerializer):
    image=serializers.ImageField()
    class Meta:
        model = TechnicianProfile
        fields = ['image']
    
    
    
    
    
class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ['date', "am8","am9",'am10',"am11","am12","pm1","pm2","pm3","pm4","pm5","pm6","pm7"]
        
    # def to_representation(self, instance):
    #     """
    #     Override the to_representation method to return data as a list of lists.
    #     """
    #     representation = super().to_representation(instance)
        
    #     # Return the field values as a list
    #     return list(representation.values())