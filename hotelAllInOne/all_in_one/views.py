from django.http import JsonResponse
from django.shortcuts import render,HttpResponse,redirect,HttpResponseRedirect, get_object_or_404
from django.contrib.auth.models import User
from all_in_one.models import Dish, hotel1, Menu, Cart,orders,Review
# from all_in_one.forms import addProductForm
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Create your views here.
def index(request):
    return render(request,'index.html')


def home(request):
    m = Menu.objects.all()
    context={'data': m}
    return render(request,'home.html',context)

def userRegister(request):
    if request.method == "GET":
        return render(request,'registerform.html')
    
    else:
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        # mobile_number = request.POST['mobile_number']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
                
        if password == confirm_password:
            
            u = User.objects.create( username = username ,first_name = first_name, last_name = last_name,  email = email ) 
            u.set_password(password)
            u.save()
            return redirect('/Userlogin')
        else:
            context = {'error':'Password are not match' }
            
            return render(request, 'registerform.html',context)
        
def user_login(request):
    if request.method == "GET":
        
        return render(request,'login.html')
    
    else:
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(username = username, password = password)
        if user is not None:
            login(request,user)
            return redirect('/')
        
        else:
            context ={'error':'User not found'}
            return render(request,'login.html',context)
        
def user_logout(request):
    logout(request)
    return redirect('/') 

#------------------ Menu Section (add dish)------------------------
@login_required(login_url='/Userlogin')
def create_menu(request):
    if request.method == "GET":
        return render(request,'create_menu.html')

    else:
        name = request.POST['name']
        description = request.POST['description']
        category = request.POST['category']
        price = request.POST['price']
        image = request.FILES['image']
       
        
        Menu = Dish.objects.create(name= name, description = description, category = category, price = price, image = image)
        Menu.save()
        return redirect('/viewMenu')
@login_required(login_url='/Userlogin')  
def updateMenu(request,rid):
    if request.method == "GET":
        p = Dish.objects.filter(id = rid)
        context = {'data':p}
        return render(request,'updateMenu.html',context)
    else:
        name = request.POST['name']
        description = request.POST['description']
        category = request.POST['category']
        price = request.POST['price']
        
        # image = request.FILES['image']
        
        UMenu = Dish.objects.filter(id = rid)
        UMenu.update(name = name, description = description, category = category, price= price)
        
        return redirect('/viewMenu')
    
    
    
@login_required(login_url='/Userlogin')
def viewMenu(request):
    menu = Dish.objects.all()
    context = {'menu': menu}
    return render(request,'viewMenu.html',context)
        
@login_required(login_url='/Userlogin')      
def deleteMenu(request,rid):
    m = Dish.objects.filter(id  = rid)
    m.delete()
    return  redirect('/viewMenu')


# --------------Hotel Section-----------------

def register_hotel(request):
    if request.method == "GET":
        return render(request,'registerHotel.html')
    else:
        H_name = request.POST['H_name']
        H_address = request.POST['H_address']  
        H_o_name = request.POST['H_o_name']
        H_image = request.FILES['H_image']
        
        
        H = hotel1.objects.create(H_name = H_name, H_address = H_address, H_onwer_name = H_o_name, H_image = H_image)
        H.save()
        return redirect('/viewHotel')
    
@login_required(login_url='/Userlogin')   
def viewHotel(request):
    # M = Dish.objects.all()
    hotel = hotel1.objects.all()
    context = {'hotel': hotel}
    
    return render(request, 'viewHotel.html',context)


# Update hotel details
@login_required(login_url='/Userlogin')
def updateHotel(request, rid):
    if request.method == "GET":
        Hotel = hotel1.objects.filter(id = rid)
        context = {'data': Hotel}
        return render(request,'updateHotel.html',context)
    else:
        H_name = request.POST['H_name']
        H_address = request.POST['H_address']  
        H_o_name = request.POST['H_o_name']
        
        H = hotel1.objects.filter(id = rid)
        H.update(H_name = H_name, H_address = H_address, H_onwer_name = H_o_name)
        return redirect('/viewHotel')


# Delete Hotel
@login_required(login_url='/Userlogin') 
def deleteHotel(request,rid):
    d = hotel1.objects.get(id = rid)
    d.delete()
    return redirect('/viewHotel')

#------------------------Main Menu Section-------------------------

@login_required(login_url='/Userlogin')
def create_main_menu(request):
    if request.method == "GET":
        dishes = Dish.objects.all()
        hotels = hotel1.objects.all()
        context = {'D_data': dishes, 'H_data': hotels}
        return render(request, "mainMenu.html", context)
    
    elif request.method == "POST":
        main_dish_id = request.POST.get('mainMenu')
        hotel_ids = request.POST.getlist('Hotel_name')
        
        try:
            dish = Dish.objects.get(id=main_dish_id)
        except Dish.DoesNotExist:
            messages.error(request, "Dish not found")
            return redirect('/mainMenu')
        
        if not hotel_ids:
            messages.error(request, "No hotels selected")
            return redirect('/mainMenu')
        
        for hotel_id in hotel_ids:
            try:
                hotel = hotel1.objects.get(id=hotel_id)
            except hotel1.DoesNotExist:
                return HttpResponse( f"Hotel with ID {hotel_id} not found")
               
            
            main_menu_exists = Menu.objects.filter(dish=dish, hotel=hotel).exists()
            if main_menu_exists:
                return HttpResponse( f"Dish is already added to {hotel.H_name}")
                
            
            Menu.objects.create(dish=dish, hotel=hotel)
        
        return redirect('/readMainMenu')
    

def read_mainMenu(request):
    m = Menu.objects.all()
    context={'data': m}
    return render(request,'readMainMenu.html',context)
    

# def delete_mainMenu(request, rid):
#     d = Menu.objects.get(id = rid)
#     d.delete()
#     return redirect('/readMainMenu')

@login_required(login_url='/Userlogin')
# def read_MainMenu_Detail(request, rid):
#     dish = get_object_or_404(Menu, id=rid)
#     hote = dish.hotel
#     all_menus = Menu.objects.filter(hotel=hote)
#     context = {}
#     context['data']=  all_menus
#     context['selected_dish'] = dish
#     return render(request, 'readMenuDetail.html', context)

def read_MainMenu_Detail(request, rid):
    dish = get_object_or_404(Menu, id=rid)
    hotel = dish.hotel
    all_menus = Menu.objects.filter(hotel=hotel)
    reviews = Review.objects.filter(product=dish)
    
    context = {
        'data': all_menus,
        'selected_dish': dish,
        'reviews': reviews,
    }
    
    return render(request, 'readMenuDetail.html', context)

# -------------------------------------- CART Section -------------------------------------------
def add_to_cart(request, rid):
    try:
        dishes = Menu.objects.get(id=rid)  # Fetch the dish by ID
    except Menu.DoesNotExist:
        return HttpResponse('Dish does not exist')

    hotels = dishes.hotel  # Fetch the hotel that assign to the dish 

    # Check if the cart contains dishes from a different hotel
    user_cart_items = Cart.objects.filter(user=request.user)
    if user_cart_items.exists():
        first_item_hotel = user_cart_items.first().menu.hotel # fetch the dish hotel 
        if first_item_hotel != hotels:
            return HttpResponse('You can only add dishes from one hotel at a time')

    # Check if the dish is already added into the cart
    cart_exists = user_cart_items.filter(menu=dishes).exists()
    if cart_exists:
        return HttpResponse('Dish is already added!!')
    
    # Proceed to add the dish to the cart
    total_price = dishes.dish.price  # Accessing the price directly from the dish object

    # Create a new cart entry
    c = Cart.objects.create(menu=dishes, user=request.user, quantity=1, total_price=total_price)
    c.save()
    
    return redirect('/readCart')


def readCart(request):
    user_cart_items = Cart.objects.filter(user=request.user)
    hotels = set(item.menu.hotel for item in user_cart_items)
    
    total_quantity = sum(item.quantity for item in user_cart_items)
    total_price = sum(item.total_price for item in user_cart_items)

    context = {
        'hotels': hotels,
        'data': user_cart_items,
        'total_quantity': total_quantity,
        'total_price': total_price,
    }

    return render(request, 'readCart.html', context)

def update_quantity(request, cart_item_id):
    cart_item = get_object_or_404(Cart, id=cart_item_id, user=request.user)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'increase':
            cart_item.quantity += 1
        elif action == 'decrease':
            cart_item.quantity = max(1, cart_item.quantity - 1)  # Ensure quantity doesn't go below 1

        cart_item.total_price = cart_item.menu.dish.price * cart_item.quantity
        cart_item.save()
    
    return redirect('/readCart')

def delete_cart(request,rid):
    c = Cart.objects.filter(id = rid)
    c.delete()
    return redirect('/readCart')


#-------------------Order section ------------------------------

def create_order(request):
    user_cart_items = Cart.objects.filter(user=request.user)
    
    #fetch the total details of the order 
    for item in user_cart_items:
        quantity = item.quantity
        total_price = item.total_price
        menu_item = item.menu
        
        order = orders.objects.create(product=menu_item, user=request.user, quantity=quantity, total_price=total_price)
        order.save()
    user_cart_items.delete()
    return redirect('/read_order')


def read_orders(request):
    user_orders = orders.objects.filter(user=request.user)
    context = {'data': user_orders}
    return render(request, 'read_order.html', context)


def create_review(request,rid):
    # menu = get_object_or_404(Menu, id=rid)
    menu = Menu.objects.filter(dish_id = rid).first()
    rev = Review.objects.filter(user = request.user, product = menu)
    
    if rev:
        return HttpResponse('Review Already added')
    else:
        if request.method == "GET":

            return render(request, 'create_review.html')
    
        else:
            title = request.POST['title']
            content = request.POST['content']
            rating = request.POST['rate']
            image = request.FILES['image']
            
            p = Menu.objects.filter(dish_id = rid).first()
            review = Review.objects.create(product = p , user = request.user ,title = title, content = content, rating = rating, image = image)
            review.save()
            return HttpResponse("Review Save")
