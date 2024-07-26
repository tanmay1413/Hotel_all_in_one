from django.urls import path
from all_in_one import views 
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    # path('', views.index),
    path('', views.home),
    path('register',views.userRegister),
    path('Userlogin',views.user_login),
    path('Userlogout', views.user_logout),
    # path('addproduct',views.addProduct),
    path('add_menu',views.create_menu),
    path('viewMenu',views.viewMenu),
    path('update_Menu/<rid>',views.updateMenu),
    path('delete_menu/<rid>',views.deleteMenu),
    path('register_hotel', views.register_hotel),
    path('viewHotel',views.viewHotel),
    path('updateHotel/<rid>',views.updateHotel),
    path('deleteHotel/<rid>', views.deleteHotel),
    path('mainMenu', views.create_main_menu),
    path('readMainMenu',views.read_mainMenu),
    path('readMenuDetail/<rid>', views.read_MainMenu_Detail),
    path('add_to_cart/<rid>', views.add_to_cart),
    path('readCart',views.readCart),
    path('remove_cart/<rid>', views.delete_cart),
    # path('update_cart/<int:cart_item_id>/', views.update_cart),
   path('update_quantity/<int:cart_item_id>/', views.update_quantity, name='update_quantity'),
   path('create_order', views.create_order),
   path('read_order', views.read_orders),
   path('create_review/<rid>', views.create_review),
   
    
    
    
    
    
    
    
    
    
    
    
    
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)