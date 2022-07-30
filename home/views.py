from django.shortcuts import render,redirect
from  .models import *
from django.views.generic import View
import datetime


# Create your views here.
class Base(View):#class used to keep common things from page
    views = {} #to store common stuffs in different pages
    views['categories'] = Category.objects.all()
    views['brands'] = Brand.objects.all()
      
    all_brand = []
    for i in Brand.objects.all():#to get value of brand
        ids = Brand.objects.get(name = i).id
            #id_brand = Brand.objects.get(slug =slug).brand
            #all_brand[i] = Product.objects.filter(brand = ids).count()
            #self.views[i] = Brand.objects.filter(name = i).count()
            #print(self.views[i])
        count = Product.objects.filter(brand = ids).count()
        all_brand.append({'product_count': count, 'ids' : ids})
    views['counts'] = all_brand

class HomeView(Base):
    def get(self, request):#get is in built method
        self.views
        self.views['sliders'] = Slider.objects.all()
        self.views['ads'] = Ad.objects.all()
        self.views['brands'] = Brand.objects.all() 
        self.views['hots'] = Product.objects.filter(labels = 'hot')
        self.views['sale'] = Product.objects.filter(labels = 'sale')
        self.views['news'] = Product.objects.filter(labels = 'new')
        return render(request, 'index.html', self.views)

class ProductDetailView(Base):
    def get(self,request,slug):#slug gets value from url 
        self.views
        self.views['details'] = Product.objects.filter(slug = slug)#slug is compared 
        self.views['reviews'] = Review.objects.filter(slug = slug)#to view review on html page
        subcat = Product.objects.get(slug = slug).subcategory #unique slug products sub cat id can be known
         
        
        self.views['subcat_products'] =  Product.objects.filter(subcategory = subcat)#get returns dictionary filter returns list
        
        
        return render(request, 'product-detail.html',self.views)
        #only special methods written inside
        
#post form is managed from this function
def review(request):
    if request.method == 'POST':
        #name = request.POST['name']
        #email = request.POST['email']
        name = request.user.username#login's username is pulled frm session 
        email = request.user.email
        review = request.POST['review']
        slug = request.POST['slug']
        x = datetime.datetime.now()
        date = x.strftime("%c")
        data = Review.objects.create(
            name = name,
            email = email,
            review = review,
            date = date,
            slug = slug
        )
        data.save()
    return redirect(f'/details/{slug}')

class CategoryView(Base):
    def get(self,request,slug):
        self.views
         
        cat_id = Category.objects.get(slug = slug).id#get gives dict
        self.views['cat_product'] = Product.objects.filter(category_id = cat_id)
        return render(request,'product-list.html',self.views)
    
class SearchView(Base):
    def get(self,request):
        self.views
        if request.method == 'GET':
            query = request.GET['query']#to search we need get 
            self.views['search_product'] = Product.objects.filter(name__icontains = query)#icontains makes title case insensitive
            self.views['search_for'] = query
        return render(request,'search.html',self.views)
    
from django.contrib.auth.models import User
from django.contrib import messages,auth
def signup(request):
    if request.method == 'POST':
        f_name = request.POST['first_name']
        l_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        
        if password == cpassword:
            if User.objects.filter(username = username).exists():
                messages.error(request,'The username is already taken')
                return redirect('/signup')#redirect send to url
            #render page lai reload
                
            elif User.objects.filter(email = email).exists():
                messages.error(request,'The email is already taken')
                return redirect('/signup')
            else:
                #make object to update and delete later on 
                data = User.objects.create_user(
                    username = username,
                    email = email,
                    password = password,
                    first_name = f_name,
                    last_name = l_name
                )
                data.save()
                return redirect('/')
        else:
            messages.error(request,'The password doesnot match')
            return redirect('/signup')
        
    return render(request,'signup.html')

from django.contrib.auth import login,logout
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username = username,password = password)#object will be empty if error
        if user is not None:#when username n password is correct
            auth.login(request,user)
            return redirect('/')
        else:
            messages.error(request, 'The username or password does not match.')
            return redirect('/login')
        
    return render(request,'login.html')
                    
                    
def logout(request):
    auth.logout(request)
    return redirect('/')

def cal(slug):
    price = Product.objects.get(slug = slug).price
    discounted_price = Product.objects.get(slug = slug).discounted_price
    if discounted_price > 0:
        actual_price = discounted_price
        
    else:
        actual_price = price
         
    try:
        quantity = Cart.objects.get(slug = slug).quantity
    except:
         
        return actual_price
    
     
        
    return actual_price,quantity
#to add product to cart in ur own, not buy but keepin basket , slug defines which product to buy
#checkout checks to buy thing or not later becomes false
from django.contrib.auth.decorators import login_required
@login_required(login_url='/login')
def add_to_cart(request,slug):
    username = request.user.username#take  username
    if Cart.objects.filter(slug = slug,username = username, checkout = False).exists():#checks if slug matches or not slug obtained from url
        #if product already kept in cart
        #price = Product.objects.get(slug = slug).price
        #discounted_price = Product.objects.get(slug = slug).discounted_price
        actual_price, quantity = cal(slug)
        #quantity = Cart.objects.get(slug = slug).quantity
        quantity = quantity + 1
        #if discounted_price > 0:
         #   actual_price = discounted_price
          #  total = quantity * actual_price
        #else:
         #   actual_price = price
          #  total = price * quantity
        total = actual_price * quantity
        Cart.objects.filter(slug = slug,username = username, checkout = False).update(
            quantity = quantity,
            total = total
        
        )    
    else:#when first time product is added
        actual_price = cal(slug)
        data = Cart.objects.create(
            username = username,
            slug = slug,
            total = actual_price,
            items = Product.objects.filter(slug = slug)[0]#get first index. inside list is dictionary
        )
        data.save()
    return redirect('/my_cart')
 
#to delete cart   
def delete_cart(request,slug):
    username = request.user.username
    Cart.objects.filter(slug = slug,username = username, checkout = False).delete()
    return redirect('/my_cart')
    
def remove_cart(request,slug):
    username = request.user.username#take  username
    if Cart.objects.filter(slug = slug,username = username, checkout = False).exists():
        actual_price, quantity = cal(slug)
        if quantity > 1:
            quantity = quantity - 1
            total = actual_price * quantity
            Cart.objects.filter(slug = slug,username = username, checkout = False).update(
                quantity = quantity,
                total = total
        
            )
    return redirect('/my_cart')


class CartView(Base):
    def get(self,request):
        username = request.user.username
        self.views['my_carts'] = Cart.objects.filter(username = username, checkout = False)
        self.views['wish_list'] = Cart.objects.filter(username = username, checkout = False)
        l = Cart.objects.filter(username = username, checkout = False).count()
        grand_total = 0
        for i in range (l):#filter provides list 
            #get only provides one value
            data = Cart.objects.filter(username = username, checkout = False)[i].total
            grand_total += data
        self.views['grand_total'] = grand_total  
        
        return render(request,'cart.html',self.views)



def base():
    views={}
     
    views['informations'] = Information.objects.all().order_by('-id')[0:1] 
     
    return views   
    

def contact(request):
    
    #views = {}
    
    if request.method == "POST":
        na  = request.POST['name']
        em = request.POST['email']
        com = request.POST['comment']
        mes = request.POST['message']
        
        data = Contact.objects.create(
           
            name = na,
            email = em,
            comment = com,
            message = mes
        )
         
        
        data.save() 
        messages.error(request,'The message has been sent.')
        return redirect('/contact')
        
         
    
    return render(request,'contact.html',base())
    
    #return render(request,'contact.html',views)






class WishView(Base):
    def get(self,request):
        username = request.user.username
       
        self.views['wish_list'] = Wish.objects.filter(username = username, checkout = False)
        l = Wish.objects.filter(username = username, checkout = False).count()
        grand_total = 0
        for i in range (l):  
             
            data = Wish.objects.filter(username = username, checkout = False)[i].total
            grand_total += data
        self.views['grand_total'] = grand_total  
        return render(request,'wishlist.html',self.views)
    

def calc(slug):
    price = Product.objects.get(slug = slug).price
    discounted_price = Product.objects.get(slug = slug).discounted_price
    if discounted_price > 0:
        actual_price = discounted_price
        
    else:
        actual_price = price
         
    try:
        quantity = Wish.objects.get(slug = slug).quantity
        #print(quantity)
    except:
         
        return actual_price
    return actual_price,quantity

@login_required(login_url='/login')
def add_to_wish_list(request,slug):
    username = request.user.username 
    if Wish.objects.filter(slug = slug,username = username, checkout = False).exists(): 
        actual_price, quantity = calc(slug)
        
        quantity = quantity + 1
         
        total = actual_price * quantity
        Wish.objects.filter(slug = slug,username = username, checkout = False).update(
            quantity = quantity,
            total = total
        
        )    
    else: 
        actual_price = calc(slug)
        data = Wish.objects.create(
            username = username,
            slug = slug,
            total = actual_price,
            items = Product.objects.filter(slug = slug)[0] 
        )
        data.save()
    return redirect('/wish-list')

def delete_wish(request,slug):
    username = request.user.username
    Wish.objects.filter(slug = slug,username = username, checkout = False).delete()
    return redirect('/wish-list')
    
def remove_wish(request,slug):
    username = request.user.username#take  username
    if Wish.objects.filter(slug = slug,username = username, checkout = False).exists():
        actual_price, quantity = calc(slug)
        if quantity > 1:
            quantity = quantity - 1
            total = actual_price * quantity
            Wish.objects.filter(slug = slug,username = username, checkout = False).update(
                quantity = quantity,
                total = total
        
            )
    return redirect('/wish-list')

#def checkout(request):
    if request.method == 'POST':
         
        username = request.POST['username']
        email = request.POST['email']
        address = request.POST['address']
        mobile = request.POST['mobile']
        country = request.POST['country']
        city= request.POST['city']
        state = request.POST['state']
        zip = request.POST['zip']
        
        data = Checkout.objects.create(
                    username = username,
                    email = email,
                    address = address,
                    mobile = mobile,
                    country =country,
                    city = city,
                    state = state,
                    zip = zip
                )
        data.save()
        
    
        messages.error(request,'The password doesnot match')
        return redirect('/checkout')
        
    return render(request,'checkout.html')

#class CheckoutView(Base):
    #def get(self,request,slug):
        #username = request.user.username
        #self.views['check_out'] = Cart.objects.filter(username = username, checkout = False)
        
        #l = Cart.objects.filter(username = username, checkout = False).count()
        #grand_total = 0
        #for i in range (l): 
         #   data = Cart.objects.filter(username = username, checkout = False)[i].total
          #  grand_total += data
        #self.views['grand_total'] = grand_total  
        #price = Product.objects.get(slug = slug).price
        #self.views['price'] = price 
        #return render(request,'checkout.html',self.views)
from django.core.exceptions import ObjectDoesNotExist       
class CheckoutView(Base):
    def get(self,request):
        username = request.user.username
        self.views['check_out'] = Cart.objects.filter(username = username, checkout = False)
        l = Cart.objects.filter(username = username, checkout = False).count()
        grand_total = 0
        for i in range (l): 
            data = Cart.objects.filter(username = username, checkout = False)[i].total
            grand_total += data
        self.views['grand_total'] = grand_total  
        #price = Product.objects.get(slug = slug).price
        #self.views['price'] = price 
        return render(request,'checkout.html',self.views)
         
         
        

    def post(self, request):
        #form = Checkout(self.request.POST or None)
        username = request.user.username
        try:
            #order = Cart.objects.filter(username = username, checkout=False)
             
            if request.method == 'POST':
                username = request.POST['username']
                email = request.POST['email']
                address = request.POST['address']
                mobile = request.POST['mobile']
                country = request.POST['country']
                city= request.POST['city']
                state = request.POST['state']
                zip = request.POST['zip']
                payment = request.POST['payment']

                if username == "" or email == "" or address=="" or mobile=="" or country=="" or city=="" or state=="" or zip=="" or payment=="":
                    messages.warning(self.request, "Failed Chekout")
                    return redirect('/check_out')
                         
                else:
                     
                    checkout_address = Checkout.objects.create(
                            username = username,
                            email = email,
                            address = address,
                            mobile = mobile,
                            country =country,
                            city = city,
                            state = state,
                            zip = zip,
                            payment=payment
                            
                        )
                    checkout_address.save()
                
                    messages.warning(self.request, "Order has been made")
                    return redirect('/check_out')

        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an order")
            return redirect("/my_cart")
    