from rest_framework import generics
from rest_framework.response import Response
from .models import TechnicianProfile
from .serializers import TechniciansProfileSerializer
from django.contrib.auth.models import User
import json
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.crypto import get_random_string
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from Users import models as users_models
from Users import serializers as users_serializers

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class TechnicianslistPagination(PageNumberPagination):
    page_size = 15  # Number of items per page
    page_size_query_param = 2  # Allow client to set custom page size
    max_page_size = 100  # Set a maximum limit
    print('oiosdonhipo')
class Technicianslist(generics.ListAPIView):
    queryset = TechnicianProfile.objects.all()
    serializer_class = TechniciansProfileSerializer
    pagination_class = TechnicianslistPagination  # Add pagination here
    print('oiosdonhipo')
    def get(self, request, *args, **kwargs):
        # Paginate the queryset
        page = self.paginate_queryset(self.get_queryset())
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            column_names = self.get_serializer().Meta.fields
            response_data = {
                "column_names": column_names,
                "data": serializer.data,
            }
            return self.get_paginated_response(response_data)  # Return paginated response

        # If no pagination is applied
        serializer = self.get_serializer(self.get_queryset(), many=True)
        column_names = self.get_serializer().Meta.fields
        response_data = {
            "column_names": column_names,
            "data": serializer.data,
        }
        return Response(response_data)



@api_view(['POST'])
def NewTechnician(request):
    data=json.loads(request.body)
    if data is None:
        return Response({'success':False})
    
    name=data.get('name')
    phone=data.get('phone')
    altphone=data.get('altphone')
    gender=data.get('gender')
    password=data.get('pass')
    
    
    if User.objects.filter(username=phone).exists():
        return Response({'success':False,'message':'Technician With Same Phone Number Already Exists Please change Phone number'})
    user=User.objects.create_user(username=phone,password=password)
    user.save()
    tecnician=TechnicianProfile.objects.create(name=name,phone=phone,alt_phone=altphone,gender=gender,userObj=user)
    tecnician.save()
    
    return Response({'success':True})



@api_view(['POST'])
def Authenticate(request):
    data=json.loads(request.body)
    username=data.get('userid')
    password=data.get('password')
    print(username,password,)
    user=authenticate(username=username,password=password)
    
    if user is None:
        print('no success')
        return Response({'success':False,'sessionid':'','message':'login failed'})
    else:
        print('success')
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        return Response({
            'success': True,
            'message': 'User login successfull',
            'sessionid': access_token,
            'refresh_token': str(refresh),
        })
        
        
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addlocation(request):
    data=json.loads(request.body)
    lat=data.get('lat')
    lon=data.get('lon')
    print(lat,lon)
    user=User.objects.get(username=request.user)
    tprofile=TechnicianProfile.objects.get(userObj=user)
    tprofile.longitude=lon
    tprofile.lattitude=lat
    tprofile.save()
    return Response({'success':True})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def adddeviceid(request):
    data=json.loads(request.body)
    deviceid=data.get('deviceid')
    technician=TechnicianProfile.objects.get(userObj=User.objects.get(username=request.user))
    print(technician)
    print(deviceid)
    technician.deviceid=deviceid
    technician.save()
    return Response({'success':True})   
    


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addaddressline(request):
    data=json.loads(request.body)
    addressline=data.get('address')
    Technician=TechnicianProfile.objects.get(user=User.objects.get(username=request.user))
    Technician.addressline=addressline
    Technician.save()
    return Response({'success':True,'message':' '})



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def fetchlocation(request):
    user=User.objects.get(username=request.user)
    tprofile=TechnicianProfile.objects.get(userObj=user)
    lon=tprofile.longitude
    lat=tprofile.lattitude
    print(lon,lat)
    working=tprofile.isworking
    return Response({'success':True,'lon':str(lon),'lat':str(lat),'message':'Success','name':tprofile.name,'isworking':working})




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def home(request):
    name=TechnicianProfile.objects.get(userObj=User.objects.get(username=request.user)).name
    todaysearnings=784
    overallearnings=78582
    return Response({'success':True,'todays':todaysearnings,'overall':overallearnings,'name':name})




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def profile(request):
    technician=TechnicianProfile.objects.get(userObj=User.objects.get(username=request.user))
    return Response({'success':True,
                     'name':technician.name,
                     'alt_phone':technician.alt_phone,
                     'phone':technician.phone,
                     'gender':technician.gender})
    
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])    
def logout(request):
    
    try:
        data=json.loads(request.body)
        refresh_token = data.get("refreshtoken")
        print(refresh_token)
        token = RefreshToken(refresh_token)
        token.blacklist()
       
        return Response({'success': True, 'message': 'Successfully logged out'})
    
    except Exception as e:
        return Response({'success': False, 'error': str(e)}, status=400)
    




from datetime import datetime, timedelta

from datetime import datetime

def time_difference_in_minutes(date_str, time_str):
    # Define current time
    current_time = datetime.now()

    try:
        given_date = datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        return "Invalid date format. Use 'YYYY-MM-DD'."

    # Convert the time part to 24-hour format
    try:
        given_time = datetime.strptime(time_str, '%I%p').time()
    except ValueError:
        return "Invalid time format. Use times like '7am', '1pm'."

    # Combine date and time to create a full datetime object
    given_datetime = datetime.combine(given_date, given_time)

    # Calculate the difference
    time_gap = given_datetime - current_time
    
    # Check if the given date and time are in the future or the past
    if time_gap.days < 0:
        return -1
    
    # Calculate the total minutes
    total_minutes = time_gap.days * 1440 + time_gap.seconds // 60  # 1440 minutes in a day
    
    return total_minutes


# Example usage


@api_view(['POST'])
@permission_classes([IsAuthenticated])   
def works(request):
    userid=request.user
    print(userid)
    technician=TechnicianProfile.objects.get(userObj=User.objects.get(username=userid))
    works=users_models.Issues.objects.filter(technician=technician).exclude(status='Fixed')
   
    date_str = '2024-11-12'
    time_str = '7pm'


    
    workslist=[]
    for i in works:
        maincategory=users_serializers.ProductsMainCategoriesSerializer(i.subcategory.maincategory).data
        timeleft=time_difference_in_minutes(str(i.date),i.time)
        print(timeleft)
        if timeleft<60:
            color='red'
        elif timeleft<120:
            color='orange'
        else:
            color='white'
        workslist.append({'image':maincategory['image'],'categoryname':maincategory['categoryname'],'date':i.date,'time':i.time,'id':i.id,'status':i.status,'color':color})
    red=[]
    orange=[]
    white=[]
    for i in workslist:
        if i['color']=='red':
            red.append(i)
        elif i['color']=='orange':
            orange.append(i)
        else:
            white.append(i)
    
    return Response({'success':True,'message':'','works':red+orange+white})




@api_view(['POST'])
@permission_classes([IsAuthenticated])   
def workdetails(request):
    data=json.loads(request.body)
    issueid=data.get('issueid')
    issue=users_models.Issues.objects.get(id=issueid)
    maincategory=users_serializers.ProductsMainCategoriesSerializer(issue.subcategory.maincategory).data
    serialized=users_serializers.IssuesSerializer(issue).data
    useraddress=users_models.UserAddress.objects.get(user=issue.user.user)
    return Response({'success':True,
                     'message':'',
                     'maincatname':maincategory['categoryname'],
                     'maincatimage':maincategory['image'],
                     'subcatname':issue.subcategory.categoryname,
                     'subcatdescription':issue.subcategory.description,
                     'customerlat':useraddress.lattitude,
                     'customerlon':useraddress.longitude,
                     'customername':issue.user.name,
                     'customerphone':issue.user.phone,
                     'audio':serialized['audio'],
                     'time':issue.time
                     })


from firebase_admin import messaging

def send_notification_to_device(device_token, title='', body='', data=None):

    message = messaging.Message(
        notification=messaging.Notification(
            title='test notification',
            body='notification pushing success',
        ),
        token=device_token,  
        data=data or {}       
    )
    try:
        response = messaging.send(message)
        print(f"Notification sent successfully: {response}")
    except Exception as e:
        print(f"Error sending notification: {e}")



@api_view(['POST'])
@permission_classes([IsAuthenticated])   
def setstatus(request):
    data=json.loads(request.body)
    issueid=data.get('issueid')
    remark=data.get('remark')
    status=data.get('status')
    issue=users_models.Issues.objects.get(id=issueid)
    issue.technicianremark=remark
    issue.status=status
    issue.save()
    return Response({'success':True,'message':' '})




@api_view(['POST'])
@permission_classes([IsAuthenticated])  
def addcharges(request):
    data=json.loads(request.body)   
    issueid=data.get('issueid')
    sparecost=data.get('sparecost')
    servicecost=data.get('servicecost')
    issue=users_models.Issues.objects.get(id=issueid)
    issue.servicecost=servicecost
    issue.sparecost=sparecost
    issue.totalcost=float(servicecost)+float(sparecost)
    issue.save()
    return Response({'success':True,'message':' '})
    
    
    
@api_view(['GET']) 
@permission_classes([IsAuthenticated])
def setworking(request):
    TechnicianProfileobj=TechnicianProfile.objects.get(userObj=User.objects.get(username=request.user))
    if TechnicianProfileobj.isworking:
        TechnicianProfileobj.isworking=False
    else:
        TechnicianProfileobj.isworking=True
    TechnicianProfileobj.save()
    return Response({'success':True,'message':'You are currently working '})
    
    
    


