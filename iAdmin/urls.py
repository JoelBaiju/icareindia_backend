from django.urls import path
from . import views

urlpatterns = [
    path('userslist',views.userslist.as_view(),name='userslist'),
    path('issuelist',views.Issuelist.as_view(),name='issuelist'),
    path('search',views.search.as_view(),name='search'),
    path('updatetechnician',views.updatetechnician,name='updatetechnician'),
    path('resetpass',views.resetpass,name='resetpass'),
    path('adminlogin',views.adminlogin,name='adminlogin'),
    path('maincategories',views.maincategories,name='maincategories'),
    path('subcategories',views.subcategories,name='subcategories'),
    path('downloadapp',views.serveicareApp,name='downloadapp')
]

