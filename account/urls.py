from django.urls import path

from . import views

urlpatterns = [
    path('',views.dashboard,name='home'),
    path('contact/',views.contact),
    path('product/',views.product,name='product'),
    path('customer/<str:pk>/',views.customer,name='customer'),
    path('order-form/<str:pk>/',views.orderform,name='order-form'),
    path('update-order/<str:pk>/',views.updateOrder,name='update-order'),
    path('delete-order/<str:pk>/',views.deleteOrder,name='delete-order'),

    path('login/',views.loginUser,name='login'),
    path('register/',views.register,name='register'),
    path('logout/',views.logoutUser,name='logout'),

    path('user/',views.userProfile,name = 'user'),

    path('account/',views.accountSettings,name='account'),

]