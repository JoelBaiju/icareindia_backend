
from django.contrib import admin
from django.urls import path,include
import Technicians.urls
import Users,Technicians
from django.conf.urls.static import static
from . import settings
import iAdmin.urls as iurls

import Users.urls
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # JWT Token views
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    # other paths...
    path('admin/', admin.site.urls),
    path('iadmin/',include(iurls)),
    path('users/', include(Users.urls)),  
    path('technicians/',include(Technicians.urls)),

]
    
    
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
