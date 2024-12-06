from django.urls import path
from . import views

urlpatterns = [
    path('signup',views.signup_request_1 ,name='signup')  ,
    path('resendotp',views.resendotp,name='resendotp'),    
    path('verifyotp',views.verifyotp,name='verifyotp'),
    path('signup2',views.signup_request_2,name='signup2'),
    path('addlocation',views.addlocation,name='addlocation'),
    path('home',views.home,name='home'),
    path('homecategories',views.homecategories.as_view(),name='homecategories'),
    path('homesubcategories',views.homesubcategories,name='homesubcategories'),
    path('find',views.find,name='find'),
    path('issuedetails',views.issuepagedatails,name='issuedetails'),
    path('registerissue',views.registerissue,name='registerissue'),
    path('profile',views.profile,name='profile'),
    path('logout',views.logout,name='logout'),
    path('delete',views.deleteaccount,name='delete'),
    path('addtimeslot',views.addtimeslot,name='addtimeslot'),
    path('myservices',views.myservices,name='myservices'),
    path('servicedetails',views.servicedetails,name='servicedetails'),
    path('raiseticket',views.raiseticket,name='raiseticket'),
    path('payment',views.payment,name='payment'),
    path('availabletechnicians',views.assigntechnician,name='availabletechnicians'),
    path('availableslots',views.availableslots,name='availableslots'),
    path('addprefferedtime',views.addprefferedtime,name='addprefferedtime'),
    path('addaddressline',views.addaddressline,name='addaddressline')
    
    

]


