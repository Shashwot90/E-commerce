from .models import *
 
from django.contrib.auth.models import User
from rest_framework import serializers 

# Serializers define the API representation.
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__" #all fields take part