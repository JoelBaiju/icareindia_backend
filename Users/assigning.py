from datetime import timedelta

from django.utils import timezone  # for timezone-aware date handling
from datetime import datetime


import requests
from django.http import JsonResponse
import math



from .search_trie import Trie

from .models import (
    UserProfile, 
    UserAddress, 
    UserTokens, 
    ProductsMainCategories, 
    ProductSubcategories,
    TechnicianAcceptedServices, 
    Issues,
    Tickets
)
from Technicians.models import  Schedule,TechnicianProfile,TechniciansEarnings
from .serializers import (
    ProductsMainCategoriesSerializer, 
    ProductSubcategoriesSerializer,
    IssuesSerializer,
    TechnicianFromIssuesSerializer
)
from Technicians.serializers import ScheduleSerializer,TechniciansProfileSerializer






from django.contrib.auth.models import User
from django.db.models import Q








    
    
    
from django.db.models import Func, F,FloatField

class DistanceCalculation(Func):
    function = 'calculate_distance'  # The custom function you created in MySQL
    template = "%(function)s(%(expressions)s)"
    output_field = FloatField() 
from django.db.models import F


def get_technicians_within_50km_radius(technicians, lon,lat, radius=50):
    technicians = technicians.annotate(
        distance=DistanceCalculation(F('lattitude'), F('longitude'), float(lat), float(lon))
    ).filter(distance__lte=radius).exclude( isworking=False )
    return technicians







def getdist(lon1, lat1, technician_location):
    # Build a semicolon-separated list of destination coordinates
    coordinates_str = ';'.join([f"{i[1]},{i[0]}" for i in technician_location])
    # print(coordinates_str)  # Debugging: check if coordinates are correctly formatted
    
    # OSRM URL for the 'route' endpoint with multiple destinations
    url = f'http://router.project-osrm.org/route/v1/driving/{lon1},{lat1};{coordinates_str}?overview=false&alternatives=false&steps=false'
    
    # Send GET request to OSRM API
    response = requests.get(url)
    
    # # Parse the response and get the distances (in meters)
    try:
        distances =response.json()['routes'][0]['legs']
    except : return False
    # print(distances)
    # Return the list of distances in kilometers (divide by 1000)
    return [dist['distance'] / 1000 for dist in distances]







from datetime import datetime, timedelta

from datetime import datetime

def time_difference_in_minutes(date_str, time_str):
    current_time = datetime.now()
 
    try:
        given_date = datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        return "Invalid date format. Use 'YYYY-MM-DD'."

    try:
        given_time = datetime.strptime(time_str, '%I%p').time()
    except ValueError:
        return "Invalid time format. Use times like '7am', '1pm'."

    given_datetime = datetime.combine(given_date, given_time)
    time_gap = given_datetime - current_time
    
    if time_gap.days < 0:
        return -1
    total_minutes = time_gap.days * 1440 + time_gap.seconds // 60  # 1440 minutes in a day
    
    return total_minutes






def availabletimeslots(useraddress,issueid):
    print(issueid)
    category=Issues.objects.get(id=issueid).subcategory.maincategory
    print(useraddress.longitude,useraddress.lattitude)
    technicians_who_serve_the_category = TechnicianProfile.objects.filter(id__in=TechnicianAcceptedServices.objects.filter(category=category).values('technician'))


    print(technicians_who_serve_the_category)    
    
    technicians_within_radius = get_technicians_within_50km_radius(technicians_who_serve_the_category,useraddress.longitude, useraddress.lattitude, 50)  
    technicianlocation = [(float(technician.lattitude),float(technician.longitude))    for technician in technicians_within_radius   ]
    
    technician_distances = getdist(useraddress.longitude,useraddress.lattitude,technicianlocation)
    if technician_distances==False:
        return False
    final_list_of_technicians=[]
    
    for i in range(len(technician_distances)):
        if technician_distances[i]<=10:
            final_list_of_technicians.append(technicians_within_radius[i])
    # print(technician_distances)
    
    # print(technicians_within_radius)
    # print(technicianlocation)
    # print(final_list_of_technicians)
    
    
    
    total_number_of_technicians_in_the_area=len(final_list_of_technicians)
    # print(total_number_of_technicians_in_the_area)
    
    
    
    today = timezone.now().date()
    seven_days_from_today = today + timedelta(days=7)
    issues_registered_from_today_to_seven_days=Issues.objects.filter(date__range=(today, seven_days_from_today),technician__in =technicians_within_radius)
    # print(issues_registered_from_today_to_seven_days.filter(date='2024-11-08',time='pm4').count())
    
    
    
    timeslots=["8am","9am","10am","11am","12pm","1pm","2pm","3pm","4pm","5pm","6pm","7pm"]
    dates=[today+timedelta(days=i) for i in range(1)]
    dates = [date.strftime('%Y-%m-%d') for date in dates]
    # print(dates)

    
    
    availableslots=[]
    today=True
    for i in dates:
        
        slots=[]
        for j in timeslots:
            if today:
                if time_difference_in_minutes(str(i),str(j)) >0:
                    pass
                else:
                    continue
            count=issues_registered_from_today_to_seven_days.filter(date=i,time=j).count()
            # print(total_number_of_technicians_in_the_area,count)
            if count< total_number_of_technicians_in_the_area:
                
                slots.append(j)
        availableslots.append({'date':i,'timeslots':slots})

            
            
    return [availableslots,final_list_of_technicians]
    
    










from firebase_admin import messaging

def send_notification_to_device(device_token, title='', body='', data=None):

    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        token=device_token,  
        data=data or {}       
    )
    try:
        response = messaging.send(message)
        print(f"Notification sent successfully: {response}")
    except Exception as e:
        print(f"Error sending notification: {e}")




from django.db.models import Sum


def assigntechnician(username,issueid,time,date,availabletechnicians):
    
    
    
    useraddress=UserAddress.objects.get(user=User.objects.get(username=username))
    
        
    today = timezone.now().date()
    seven_days_from_today = today + timedelta(days=7)
    FinallyFinalList=[]
    for i in availabletechnicians:
        # print(i)
        if Issues.objects.filter(date=date,time=time,technician=i.id).exists():
            pass
        else:
            FinallyFinalList.append(i)
    
    
    
    current_date = datetime.now()
    month = current_date.month
    year = current_date.year

    technician_lowest_income=10000000000
    technician=None
    
    for i in FinallyFinalList :
        # print(i)
        # Filter records for the current month and year, and calculate the total earnings
        total_income = TechniciansEarnings.objects.filter(
            technician=i,
            date__year=year,
            date__month=month
        ).aggregate(total_earnings=Sum('earnings'))['total_earnings']
        
        # print(total_income)
        if total_income==None or total_income<technician_lowest_income :
            technician=i
            technician_lowest_income=total_income
            
    # print(technician,technician_lowest_income)
    print(issueid)
    issue=Issues.objects.get(id=issueid)
    issue.technician=technician
    issue.date=date
    issue.time=time
    issue.save()
    send_notification_to_device(title='Work Assigned' , body='You have a new Work Assigned' , device_token=technician.deviceid)
    print(FinallyFinalList)
    
    

    


    