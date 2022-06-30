from tokenize import blank_re
from unicodedata import category
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.name 

class Customer(models.Model):
    user = models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=200,null=True)
    phone = models.CharField(max_length=200,null=True)
    email = models.CharField(max_length=200,null=True)
    profile_pic = models.ImageField(null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.name 
    

class Product(models.Model):
    CETAGORY = (
        ('Indoor','Indoor'),
        ('Outdoor','Outdoor'),
    )
    name = models.CharField(max_length=200,null=True)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=200,null=True,choices=CETAGORY)
    description = models.CharField(max_length=300,null=True,blank=True)
    tag = models.ManyToManyField(Tag)
    date_created = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS = (
        ('Pending','Pending'),
        ('Out for Delivery','Out for Delivery'),
        ('Delevered','Delevered'),

    )
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True)
    Product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    date_created = models.DateTimeField(auto_now_add=True,null=True)
    status = models.CharField(max_length=200,null=True,choices=STATUS)
    note = models.CharField(max_length=1000,null=True,blank=True)

    def __str__(self):
        return self.Product.name +" >> "+ self.status
    
