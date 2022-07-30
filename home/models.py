from django.db import models
from django.forms import CharField, ImageField, IntegerField
from djrichtextfield.models import RichTextField
from django_countries.fields import CountryField

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length = 200)
    icon = models.CharField(max_length = 200)
    #slug is an id it should be unique
    #imp for SEO shown in link like /smartphones/samsung
    slug = models.TextField(unique = True)
    
    def __str__(self):
        return self.name
    
class SubCategory(models.Model):
    name = models.CharField(max_length = 200)
    #use foreign key
    category = models.ForeignKey(Category,on_delete = models.CASCADE)#category is field. accesses Category. deltes subcategory as well when category is deleted. 
    #CASCASE is keyword
    icon = models.CharField(max_length = 200, blank = True)
    #slug is an id it should be unique
    #imp for SEO shown in link like /smartphones/samsung
    slug = models.TextField(unique = True)
    
    
    
    def __str__(self):
        return self.name
 
 
#status is static. static data needs tuple. only two values    
STATUS = (('active','Active'),('','Default'))   
class Slider(models.Model):
    name = models.CharField(max_length = 200)
    image = models.ImageField(upload_to = 'media')#makes folder named media and keeps photo on folder
    text = models.TextField(blank = True)
    rank = models.IntegerField()
    status = models.CharField(choices = STATUS, blank = True, max_length = 100)
    
    def __str__(self):
        return self.name
    
class Ad(models.Model):
    name  = models.CharField(max_length = 400)
    image = models.ImageField(upload_to = 'media')
    text = models.TextField(blank = True)
    rank = models.IntegerField()
    
    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length = 400)
    image = models.ImageField(upload_to = 'media')
    rank  = models.IntegerField()
    
    def __str__(self):
        return self.name

LABELS = (('new','New'),('hot','Hot'),('sale', 'Sale'),('','default'))    
STOCK = (('In Stock','In Stock'),('Out of Stock','Out of Stock')) 
class Product(models.Model):
    name = models.CharField(max_length = 400)
    price = models.IntegerField()
    discounted_price = models.IntegerField(default = 0)
    category = models.ForeignKey(Category,on_delete = models.CASCADE)
    subcategory = models.ForeignKey(SubCategory,on_delete = models.CASCADE)
    brand = models.ForeignKey(Brand,on_delete = models.CASCADE,default = 1)
    image = models.ImageField(upload_to ='media')
    description = RichTextField()
    specification = RichTextField()
    slug = models.TextField(unique = True)
    labels = models.CharField(choices = LABELS, max_length = 100)
    stock = models.CharField(choices = STOCK, max_length = 100)
    
    def __str__(self):
        return self.name
    
class Review(models.Model):
    name = models.CharField(max_length = 400)
    email = models.EmailField(max_length = 400)
    review = models.TextField(blank = True)
    date = models.CharField(max_length=200)    
    slug = models.TextField()
    point = models.IntegerField(default = 1)
    
    def __str__(self):
        return self.name
    
    
class Cart(models.Model):
    username = models.CharField(max_length = 300)
    slug = models.TextField(max_length = 500)
    quantity = models.IntegerField(default = 1)
    total = models.FloatField()
    checkout = models.BooleanField(default = False)
    items = models.ForeignKey(Product,on_delete = models.CASCADE)
    
    def __str__(self):
        return self.username
    
class Information(models.Model):
    address1 = models.CharField(max_length = 500)
    address2 = models.CharField(max_length = 500, blank = True )# this is non required field. this can be left empty.
    phone = models.CharField(max_length = 50)
    time = models.CharField(max_length = 100)
    email = models.CharField(max_length = 200)
    
    def __str__(self):
        return f"{self.address1} {self.address2}"
    
class Contact(models.Model):#Model is object class called with help of it
    name = models.CharField(max_length = 300)
    email = models.EmailField(max_length = 200)
    comment = models.TextField()#dynamic length
    message = models.TextField()
    
    def __str__(self):#string repressentation of an object
        return self.name


class Wish(models.Model):
    username = models.CharField(max_length = 300)
    slug = models.TextField(max_length = 500)
    quantity = models.IntegerField(default = 1)
    total = models.FloatField()
    checkout = models.BooleanField(default = False)
    items = models.ForeignKey(Product,on_delete = models.CASCADE)
    
    def __str__(self):
        return self.username
    

class Checkout(models.Model):
    username = models.CharField(max_length = 300)
    email = models.EmailField(max_length = 200)
    mobile = models.CharField(max_length = 300)
    address = models.CharField(max_length = 300)
     
    country = CountryField(blank_label='(select country)')
    city = models.CharField(max_length = 300)
    state =  models.CharField(max_length = 300)
    zip = models.CharField(max_length = 300)
    payment = models.CharField(max_length = 300,default = 1)
    #payment_option = models.BooleanField(widget=models.RadioSelect())
    def __str__(self):
        return self.username