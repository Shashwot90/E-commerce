# ViewSets define the view behavior.
#handles get and post request
from rest_framework import viewsets
from .models import *
from .serializers import *
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    
    
import django_filters.rest_framework
from rest_framework import filters 
from rest_framework import generics

class ProductFilterView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category','labels']
    search_fields = ['name', 'description']
    ordering_fields = ['id', 'price','name']