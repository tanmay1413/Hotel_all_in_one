from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Dish(models.Model):
    type = (("Veg",'Veg'),('Non-Veg','Non-Veg'))
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    category = models.CharField(max_length=200 ,choices=type)
    price = models.IntegerField()
    image = models.ImageField(upload_to='image')

class hotel1(models.Model):
    H_name = models.CharField(max_length=200)
    H_address = models.CharField(max_length=200)
    H_onwer_name = models.CharField(max_length=200)
    H_image = models.ImageField(upload_to='Hotel_Image')
    
class Menu(models.Model):
    
    dish =models.ForeignKey(Dish, on_delete= models.CASCADE)
    hotel = models.ForeignKey(hotel1, on_delete= models.CASCADE)
    
class Cart(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_price = models.IntegerField()


class orders(models.Model):
    product = models.ForeignKey(Menu, on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete= models.CASCADE)
    quantity = models.IntegerField()
    total_price = models.IntegerField()
    

class Review(models.Model):
    type = ((1,1),(2,2),(3,3),(4,4),(5,5))
   
    product = models.ForeignKey(Menu,on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.CharField(max_length=200)
    rating = models.IntegerField(choices=type)
    image = models.ImageField(upload_to='reviewimage', null=True, blank= True)