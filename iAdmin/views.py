from django.shortcuts import render
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

from Users.assigning import assigntechnician
from Users.search_trie import Trie

from Users.models import (
    UserProfile, 
    UserAddress, 
    UserTokens, 
    ProductsMainCategories, 
    ProductSubcategories, 
    Issues,
    Tickets
)
from Technicians.models import  Schedule,TechnicianProfile,TechniciansEarnings
from Users.serializers import (
    ProductsMainCategoriesSerializer, 
    ProductSubcategoriesSerializer,
    IssuesSerializerlist,
    TechnicianFromIssuesSerializer,
    UserProfileSerializers
)
from Technicians.serializers import ScheduleSerializer,TechniciansProfileSerializer
from rest_framework.pagination import PageNumberPagination



class UserslistPagination(PageNumberPagination):
    page_size =15   # Number of items per page
    page_size_query_param = 2  # Allow client to set custom page size
    max_page_size = 100  # Set a maximum limit
class userslist(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializers
    pagination_class = UserslistPagination  # Add pagination here
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




class IssuelistPagination(PageNumberPagination):
    page_size = 15  
    page_size_query_param = 2  
    max_page_size = 100 
class Issuelist(generics.ListAPIView):
    # queryset = Issues.objects.all()
    # print(queryset)
    serializer_class = IssuesSerializerlist
    pagination_class = IssuelistPagination
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





class search(generics.ListAPIView):
    queryset=None
    serializer_class = TechniciansProfileSerializer
    def post(self, request, *args, **kwargs):
        data=json.loads(request.body)
        try:
            self.queryset =TechnicianProfile.objects.filter(**{data[0].lower(): data[1]})
            serialized = self.get_serializer(self.get_queryset(), many=True)
            column_names = self.get_serializer().Meta.fields
            response_data = {
                "column_names": column_names,
                "data": serialized.data,
            }

        
            return Response(response_data)
        except:
            return Response({'message':'No Matching technician'})
        
        
@api_view(['POST'])
def updatetechnician(request):
    data=json.loads(request.body)
    name=data.get('name')
    altphone=data.get('altphone')
    technician=TechnicianProfile.objects.get(id=data.get('id'))
    if len(name)>3:
        technician.name=name
    if len(altphone)>=10:
        technician.alt_phone=altphone
    technician.save()
    print(name,altphone)
    return Response({'success':True})



from django.contrib.auth.hashers import make_password

@api_view(['POST'])
def resetpass(request):
    try:
        data = json.loads(request.body)
        newpass = data.get('newpass')
        technician_id = data.get('id')
        
        # Ensure both ID and password are provided
        if not newpass or not technician_id:
            return Response({'error': 'ID and new password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch technician and handle case if technician is not found
        try:
            technician = TechnicianProfile.objects.get(id=technician_id)
        except TechnicianProfile.DoesNotExist:
            return Response({'error': 'Technician not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Check password length
        if len(newpass) <= 3:
            return Response({'error': 'Password must be longer than 3 characters.'}, status=status.HTTP_400_BAD_REQUEST)

        # Hash the new password and update it
        technician.userObj.password = make_password(newpass)
        technician.userObj.save()

        return Response({'success': True}, status=status.HTTP_200_OK)

    except json.JSONDecodeError:
        return Response({'error': 'Invalid JSON.'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
def adminlogin(request):
    data=json.loads(request.body)
    phone=data.get('phone')
    password=data.get('pass')
    user= authenticate(request,username=phone,password=password)
    if user is not None:
        print(user)
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        return Response({'success':True,
                         'username':user.username,
                         'access_token':access_token,
                         'refresh_token':str(refresh)})
    else:
        return Response({'success':False})
        



@api_view(['GET'])
def maincategories(request):
    queryset = ProductsMainCategories.objects.all()
    serialized=ProductsMainCategoriesSerializer(queryset,many=True)
    response_data={
        'column_names':ProductsMainCategoriesSerializer.Meta.fields,
        'data':serialized.data
    }
    return Response(response_data)


@api_view(['POST'])
def subcategories(request):
    id=json.loads(request.body).get('maincatid')
    queryset=ProductSubcategories.objects.filter(maincategory=ProductsMainCategories.objects.get(id=id))
    serialized=ProductSubcategoriesSerializer(queryset,many=True)
    print(serialized.data)
    return Response(serialized.data)


import os
from django.http import FileResponse, Http404

@api_view(['GET'])
def serveicareApp(request):
    filepath = os.path.join('media', 'icareApp', 'icareindiaApp.apk')
    
    if not os.path.exists(filepath):
        raise Http404("File not found")
    
    response = FileResponse(open(filepath, 'rb'), as_attachment=True, filename='icareindiaApp.apk')
    return response
