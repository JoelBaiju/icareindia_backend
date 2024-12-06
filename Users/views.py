# 1. Standard library imports
import json
import random
import secrets
import string
from datetime import timedelta
import heapq



# 2. Django imports
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.cache import cache
from django.utils import timezone
import requests
from django.http import JsonResponse
from django.core.cache import cache
from django.db.models import Q

    


# 3. Third-party imports (Django REST Framework)
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status



# 4. Local application imports (your models and serializers)

from .assigning import assigntechnician
from .search_trie import Trie

from iAdmin.models import Razorpay
from .models import (
    UserProfile, 
    UserAddress, 
    UserTokens, 
    ProductsMainCategories, 
    ProductSubcategories, 
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
from Technicians.serializers import TechnicianImageSerializer,ScheduleSerializer,TechniciansProfileSerializer



def generate_random_otp(length=6):
    otp=''.join(secrets.choice(string.digits) for _ in range(length))
    print(otp)
    return otp







@api_view(['POST'])
def signup_request_1(request):
    try:
        # Parse the JSON request data
        data = json.loads(request.body)
        phone = data.get('phoneNumber')
        
        # Check if phone number is provided
        if not phone:
            return Response({'success': False, 'message': 'Phone number is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if user already exists
        exists = User.objects.filter(username=phone).exists()
        
        # Generate OTP
        otp = generate_random_otp()
        
        # Store OTP and phone number in cache with timeout (10 minutes)
        cache.set(
            f'otp_{phone}',
            value={'otp': otp, 'phone': phone, 'exists': exists},
            timeout=600  # Timeout in seconds (10 minutes)
        )
        
        return Response({'success': True, 'exists': exists})

    except json.JSONDecodeError:
        return Response({'success': False, 'message': 'Invalid JSON format.'}, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        # Log or print error for debugging purposes
        print(f"Error in signup_request_1: {str(e)}")
        return Response({'success': False, 'message': 'An error occurred while processing your request.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)











@api_view(['POST'])
def verifyotp(request):
    data = json.loads(request.body)
    phone=data.get('phoneNumber')
    otp=data.get('otp')
    

    cache_data=cache.get(f'otp_{phone}')
    print(cache_data)
    if otp==cache_data['otp']:
        print('done otp verified')
        if cache_data['exists']:
            user=User.objects.get(username=cache_data['phone'])
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)      
            print(access_token)          
            return Response({'success':True,
                             'message':'otp verified',
                             'exists':cache_data['exists'],
                             'sessionid':access_token,
                             'refresh_token':str(refresh)})
        else:
            return Response({'success':True,
                             'message':'otp verified',
                             'exists':cache_data['exists'],
                             'sessionid':'',
                             'refresh_token':''})
            
    else:
        print('otp does not match')
        return Response({'success':False,
                         'message':'otp does not match',
                         'exists':cache_data['exists'],
                         'sessionid':' '})

    
    
    




@api_view(['POST'])    
def signup_request_2(request):
    
    data=json.loads(request.body)
    phone=data.get('phoneNumber')
    name=data.get('name')
    gender=data.get('gender')
    alt_phone=data.get('alternativenumber')
    address=data.get('address')
    print(phone,name,gender)
    if User.objects.filter(username=phone).exists():
        return Response({'success':False,
                         'message':'user already exists',
                         "sessionid": '_',
                         "refresh_token":'_'})    
    
    DjangoUserobj=User.objects.create_user(
        username=phone, 
        password=phone+name+gender  
    )
    DjangoUserobj.save()
    refresh = RefreshToken.for_user(DjangoUserobj)
    access_token = str(refresh.access_token)
    
    userProfile=UserProfile.objects.create(
        name=name,
        phone=phone,
        gender=gender,
        alt_phone=alt_phone,
        user=DjangoUserobj
    )
    userProfile.save()
    
    
    address=UserAddress.objects.create(
        addressline=address,
        user=DjangoUserobj
    )
    address.save()
    print(access_token,str(refresh))
    return Response({'success':True,
                     'message':'user created successfully',
                     "sessionid": access_token,
                     "refresh_token":str(refresh)})    



@api_view(['POST'])
def resendotp(request):
    data=json.loads(request.body)
    phone=data.get('phoneNumber')
    cache_data=cache.get(f'otp_{phone}')   
    otp=generate_random_otp()
    cache.set(f'otp_{phone}', value={
                                    'otp': otp,
                                    'phone': phone,
                                    'exists': cache_data['exists']
                                    }, timeout=600) 
    print(otp)
                                    
    return Response({'success':True,'message':'Otp sent sucessfully'})
    
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addlocation(request):
    data=json.loads(request.body)
    user=User.objects.get(username=request.user)
    longitude=data.get('lon')
    lattitude=data.get('lat') 
    address=UserAddress.objects.get(user=user)
    address.longitude=longitude
    address.lattitude=lattitude
    address.save()
    return Response({'success':True,'message':'location added'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def home(request):
    data=json.loads(request.body)
    try:
        user=User.objects.get(username=request.user)
        name=UserProfile.objects.get(user=user).name
        address=UserAddress.objects.get(user=user)
        longitude=address.longitude
        lattitude=address.lattitude
        print(longitude,lattitude,name)
        return Response({'success':True,
                        'message':'Coordinates fetched and sent successfully',
                        'name':name,
                        'longitude':longitude,
                        'lattitude':lattitude})
    except:
        return Response({'success':True,
                        'message':'Coordinates fetched and sent successfully',
                        'name':'',
                        'longitude':'',
                        'lattitude':''})



class homecategories(generics.ListAPIView):
    
    queryset = ProductsMainCategories.objects.all()
    serializer_class = ProductsMainCategoriesSerializer 


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addaddressline(request):
    data=json.loads(request.body)
    addressline=data.get('address')
    addressobj=UserAddress.objects.get(user=User.objects.get(username=request.user))
    addressobj.addressline=addressline
    addressobj.save()
    return Response({'success':True,'message':' '})

@api_view(['POST'])
def homesubcategories(request):
    data=json.loads(request.body)
    categoryid=data.get('id')
    maincategoryname=ProductsMainCategories.objects.get(id=categoryid).categoryname
    subcategories=ProductSubcategories.objects.filter(maincategory=categoryid)
    serializer=ProductSubcategoriesSerializer(subcategories,many=True)

    return Response({'success':True,
                     'subcategories':serializer.data,
                     'title':maincategoryname})




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def profile(request):
    user=UserProfile.objects.get(user=User.objects.get(username=request.user))
    altphone=user.alt_phone
    if len(altphone)==0:
        altphone='Not available'
    return Response({'success':True,
                     'name':user.name,
                     'alt_phone':altphone,
                     'phone':user.phone,
                     'gender':user.gender})



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
    



@api_view(['POST'])
@permission_classes([IsAuthenticated]) 
def deleteaccount(request):
      
    try:
        data=json.loads(request.body)
        refresh_token = data.get("refreshtoken")
        print(refresh_token)
        token = RefreshToken(refresh_token)
        token.blacklist()
        user=UserProfile.objects.get(user=User.objects.get(username=request.user))
        user.delete()
        
        return Response({'success': True, 'message': 'Acount deleted successfully'})
    
    except Exception as e:
        return Response({'success': False, 'error': str(e)}, status=400)
    


def load_trie_from_cache():
    """Helper function to load Trie from cache."""
    serialized_trie = cache.get('trie')
    # print(serialized_trie)
    if serialized_trie:
        trie = Trie()
        trie.deserialize(serialized_trie)
        return trie
    return None





@api_view(['POST'])
def find(request): 
    data=json.loads(request.body) 
    keyword=data.get('key') 

    if not keyword:
        return Response({"error": "Keyword not provided"}, status=400)
    
    # Load the Trie from cache
    trie = load_trie_from_cache()
    if trie is None:
        return Response({"error": "Trie not available"}, status=500)
    
    # Search for the keyword in the Trie
    # subcategories=ProductSubcategories.objects.
    matchkeys = trie.search(keyword)
    # return Response({"result":matchkeys})
    result=[]
    for key in matchkeys:
        for category_id in key[1]:
            print(category_id)
            result.append({'name':ProductSubcategories.objects.get(id=category_id).categoryname,'id':category_id})
            
    if len(result)!=0:
        return Response({"result": result ,
                         'message':" " ,
                         'success':True})
    else:
        return Response({"message": "Keyword not found",
                         'result':[],
                         'success':False}, status=404)


@api_view(['POST'])
def issuepagedatails(request):
    data=json.loads(request.body)
    subid=data.get('id')
    print(subid)
    
    subcat=ProductSubcategories.objects.get(id=subid)
    maincat=ProductsMainCategoriesSerializer(subcat.maincategory)
    subcat=ProductSubcategoriesSerializer(subcat)
    return Response({'success':True,
                     'maincat':maincat.data,
                     'subcat':subcat.data  })




# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def registerissue(request):
#     try:
#         # Parse JSON data from the request
#         # data = json.loads(request.body)
#         issue = request.POST.get('issue')
#         subcat_id   = request.POST.get('subcatid')

   
#         audio = request.FILES.get('audio')
        # print(subcat_id,audionote,time,date)
        # Check for required fields
        
        

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def registerissue(request):
    try:
       
        # Access POST and FILES data
        issue = request.POST.get('issue')
        subcat_id = request.POST.get('subcatid')
        audio = request.FILES.get('audio')


        if not all([issue, subcat_id]):
            return Response({'success': False, 'message': 'Missing required fields.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate subcategory
        try:
            subcategory = ProductSubcategories.objects.get(id=subcat_id)
        except ProductSubcategories.DoesNotExist:
            return Response({'success': False, 'message': 'Invalid subcategory ID.'}, status=status.HTTP_404_NOT_FOUND)
        
        # Validate user profile
        try:
            user_profile = UserProfile.objects.get(user=User.objects.get(username=request.user))
        except UserProfile.DoesNotExist:
            return Response({'success': False, 'message': 'User profile not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        
        
        issue_obj = Issues.objects.create(
            issue=issue,
            audio=audio,
            status='Registered',
            subcategory=subcategory,
            user=user_profile,
          
        )
        if subcategory.maincategory.managedbyadmin:
            issue_obj.managedbyadmin=True
        else:
            issue_obj.managedbyadmin=False
        issue_obj.save()

        print(issue_obj.id)
        return Response({'success': True, 'message': 'Issue has been registered', 'issueid': issue_obj.id,'managed':subcategory.maincategory.managedbyadmin})
    except json.JSONDecodeError:
        return Response({'success': False, 'message': 'Invalid JSON format.'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(f"Error registering issue: {str(e)}")
        return Response({'success': False, 'message': 'An error occurred while registering the issue.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    
    
@api_view(['POSt'])
@permission_classes([IsAuthenticated])
def addprefferedtime(request):
    data=json.loads(request.body)
    issueid=data.get('issueid')
    prefferdtime=data.get('time')
    issue=Issues.objects.get(id=issueid)
    issue.time=prefferdtime
    issue.save()
    return Response({'success':True,'message':' '})
    
    
    
from .assigning import availabletimeslots

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def availableslots(request):
    data=json.loads(request.body)
    issueid=data.get('issueid')
    useraddress= UserAddress.objects.get(user=User.objects.get(username=request.user))
    result=availabletimeslots(useraddress,issueid) 
    if result==False:
        return Response({"success": True,
                        'schedules':[],
                        'message':'No schedules available'})
    
    cache.set(
        f'issue_{issueid}',
        value={'technicianlist':result[1]},
        timeout=6000  # Timeout in seconds(10 minutes)
    )

    return Response({"success": True,
                     'schedules':result[0],
                     'message':' '})







@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addtimeslot(request):
    data=json.loads(request.body)
    issueid=data.get('issueid')
    date=data.get('date')
    time=data.get('time')
    cachedata=cache.get(
        f'issue_{issueid}',
    )
    assigntechnician(request.user,issueid,time,date,cachedata['technicianlist'])
    return Response({'success':True,'message':' '})







@api_view(['POST'])
@permission_classes([IsAuthenticated])
def myservices(request):
    
    user=UserProfile.objects.get(user=User.objects.get(username=request.user))
    all_issues=Issues.objects.filter(user=user)
    
    for i in all_issues:
        if i.time==None:
            Issues.objects.get(id=i.id).delete()
            
    all_issues=Issues.objects.filter(user=user)
    serialized=IssuesSerializer(all_issues,many=True)
    upcomingservices=[]
    previousservies=[]
    
    for i in serialized.data:
        q=ProductSubcategories.objects.filter(id=i['subcategory'])[0].maincategory
        sq=ProductsMainCategoriesSerializer(q).data
        
        i['name']=sq['categoryname']
        i['image']=sq['image']
        if i['status']!='Fixed':
            upcomingservices.append(i)
        else:
            previousservies.append(i)
        print(upcomingservices)
        print(previousservies)

    # print(upcomingservices)
    # print(previousservies)
    # return Response({'success':True,'upcoming':' ','previous':' '})
    return Response({'success':True,
                     'upcoming':upcomingservices,
                     'previous':previousservies})



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def servicedetails(request):
    data=json.loads(request.body)
    issueid=data.get('id')
    issue=Issues.objects.get(id=issueid)    
    subcategory=issue.subcategory
    maincategory=subcategory.maincategory
    serializedmaincategory=ProductsMainCategoriesSerializer(maincategory).data
    serializedsubcategory=ProductSubcategoriesSerializer(subcategory).data
    serializedissue=IssuesSerializer(issue).data
    upoming=serializedissue['status']!='Fixed'
    try:
        Technician=TechnicianProfile.objects.get(id=issue.technician.id)
        serializedtechnicianimage=TechnicianImageSerializer(Technician)
    except:
            return Response({   
                'success':True,
                'image':serializedmaincategory['image'],
                'maincat':serializedmaincategory['categoryname'],
                'subcat':serializedsubcategory['categoryname'],
                'description':serializedsubcategory['description'],
                'spare':serializedissue['sparecost'],
                'service':serializedissue['servicecost'],
                'total':serializedissue['totalcost'],
                'upcoming':upoming,
                'id':serializedissue['id'],
                'technician':{
                    'name':'iCareIndia',
                    'image':'',
                    'phone':'+918921765007'   
                }
                
            })  
        
    print(serializedtechnicianimage.data)
    return Response({   
        'success':True,
        'image':serializedmaincategory['image'],
        'maincat':serializedmaincategory['categoryname'],
        'subcat':serializedsubcategory['categoryname'],
        'description':serializedsubcategory['description'],
        'spare':serializedissue['sparecost'],
        'service':serializedissue['servicecost'],
        'total':serializedissue['totalcost'],
        'upcoming':upoming,
        'id':serializedissue['id'],
        'technician':{
            'name':issue.technician.name,
            'image':serializedtechnicianimage.data['image'],
            'phone':issue.technician.phone   
        }
                        
    })
    
    
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def raiseticket(request):
    data=json.loads(request.body)
    issue=Issues.objects.get(id=data.get('issueid'))
    user=UserProfile.objects.get(user=User.objects.get(username=request.user))
    Tickets.objects.create(user=user,
                           ticket=data.get('ticket'),
                           issue=issue)
    
    return Response({'success':True,
                     'message':'Ticket raised successfully'})





@api_view(['POST'])
@permission_classes([IsAuthenticated])
def payment(request):
    data=json.loads(request.body)
    issueid=data.get('issueid')
    print(issueid)
    issue=Issues.objects.get(id=issueid)
    razorpaykeys=Razorpay.objects.all()
    razorpaykey=razorpaykeys[0].key
    if issue.totalcost==0:
        return Response({
            'billed':False,
            'key':'',
            'amount':'',
        })
    else:
        return Response({
            'billed':True,
            'key':razorpaykey,
            'amount':issue.totalcost,
        })
    