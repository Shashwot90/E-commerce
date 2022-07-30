from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name = 'home'),#if class based view then use  .as_views() #if function is used then no need
    path('details/<slug>', ProductDetailView.as_view(), name = 'detail'),#url gets value and url gets value through template
    path('add_review', review, name = 'add_review'),
    path('category/<slug>', CategoryView.as_view(), name = 'category'),
    path('search',SearchView.as_view(), name="search"),
    path('signup',signup, name="signup"),
    path('login',login,name='login'),
    path('logout',logout,name='logout'),
    path('add-to-cart/<slug>',add_to_cart,name = 'add-to-cart'),
    path('delete-cart/<slug>',delete_cart,name='delete-cart'),
    path('remove-cart/<slug>',remove_cart,name='remove-cart'),
    path('my_cart', CartView.as_view(), name = 'my_cart'),
    path('contact',contact, name='contact'),
    path('add-to-wish-list/<slug>',add_to_wish_list,name = 'add-to-wish-list'),
    path('delete-wish/<slug>',delete_wish,name='delete-wish'),
    path('remove-wish/<slug>',remove_wish,name='remove-wish'),
    path('wish-list',WishView.as_view(),name = 'wish-list'),
    #path('checkout',checkout, name="checkout"),
    path('check_out',CheckoutView.as_view(),name = 'check_out')
]