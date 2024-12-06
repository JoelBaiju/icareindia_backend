from django.contrib import admin
from .models import UserProfile,UserAddress,ProductsMainCategories,ProductSubcategories,UserTokens,Issues,Tickets,TechnicianAcceptedServices


admin.site.register(UserProfile)
admin.site.register(UserAddress)
admin.site.register(ProductsMainCategories)
admin.site.register(ProductSubcategories)
admin.site.register(Issues)
admin.site.register(UserTokens)
admin.site.register(Tickets)
admin.site.register(TechnicianAcceptedServices)