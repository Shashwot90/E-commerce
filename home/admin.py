from django.contrib import admin

from home.views import contact
from .models import * 
# Register your models here.
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Slider)
admin.site.register(Ad)
admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(Review)
admin.site.register(Cart)
admin.site.register(Information)
admin.site.register(Contact)
admin.site.register(Wish)
admin.site.register(Checkout)