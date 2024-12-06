from django.urls import path
from . import views

urlpatterns = [
    path('technicianslist',views.Technicianslist.as_view(),name='technicianslist'),
    path('newtechnician',views.NewTechnician,name='newtechnician'),
    path('authenticate',views.Authenticate,name='authenticate'),
    path('addlocation',views.addlocation,name='addlocation'),
    path('fetchlocation',views.fetchlocation,name='fetchlocation'),
    path('home',views.home,name='home'),
    path('profile',views.profile,name='profile'),
    path('logout',views.logout,name='logout'),
    path('works',views.works,name='works'),
    path('workdetails',views.workdetails,name='workdetails'),
    path('addcharges',views.addcharges,name='addcharges'),
    path('setstatus',views.setstatus,name='setstatus'),
    path('setworking',views.setworking,name='setworking'),
    path('adddeviceid',views.adddeviceid,name='adddeviceid'),
    path('addaddressline',views.addaddressline,name='addaddressline')
    
]

