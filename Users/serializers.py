
from rest_framework import serializers
from .models import ProductsMainCategories,ProductSubcategories,Issues,UserProfile


class UserProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model=UserProfile
        fields=['name','phone','alt_phone','gender','id']
    def to_representation(self, instance):
        """
        Override the to_representation method to return data as a list of lists.
        """
        representation = super().to_representation(instance)
        
        # Return the field values as a list
        return list(representation.values())


class ProductsMainCategoriesSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()  
    managedbyadmin=serializers.BooleanField()
    class Meta:
        model = ProductsMainCategories
        fields = ['categoryname', 'image' ,'managedbyadmin','id'] 
        

class ProductsMainCategoriesSerializer_List(serializers.ModelSerializer):
    image = serializers.ImageField()  
    class Meta:
        model = ProductsMainCategories
        fields = ['id', 'categoryname', 'image','managedbyadmin']
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return list(representation.values())
        
 
        
class ProductSubcategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSubcategories
        fields = ['id','categoryname','description']
        
class IssuesSerializerlist(serializers.ModelSerializer):
    subcategory_name = serializers.CharField(source='subcategory.categoryname', read_only=True)  # Assuming 'name' is the field in ProductSubcategories
    technician_name=serializers.CharField(source='technician.name', read_only=True) 
    class Meta:
        model = Issues
        fields = ['id', 'time', 'date', 'status', 'subcategory_name', 'servicecost', 'sparecost', 'totalcost','technician_name']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return list(representation.values())


    
class IssuesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issues
        fields=['id','time','date','status','subcategory','servicecost','sparecost','totalcost','audio']


class TechnicianFromIssuesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issues
        fields=['technician']
            
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return list(representation.values())
    
