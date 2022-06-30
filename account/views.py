from dataclasses import field
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Customer,Product,Order,Tag

from .forms import OrderForm,CreateUserForm,CustomerForm

from django.forms import inlineformset_factory
from .filters import OrderFilter
from django.contrib.auth import authenticate,login,logout

from django.contrib.auth.decorators import login_required

from .decorators import unauthenticated,user_role,admin_only

from django.contrib.auth.models import Group

# Create your views here.

@login_required(login_url='login')
@admin_only
def dashboard(request):
    customer = Customer.objects.all()
    product = Product.objects.all()
    order = Order.objects.all()
    total_order = order.count()
    delivered = order.filter(status = 'Delevered').count()
    pending = order.filter(status = 'Pending').count() 



    context = {'customers':customer,'products':product,'orders':order,'total_order':total_order,'pending':pending,'delivered':delivered} 
    return render(request,'account/dashboard.html',context)

def contact(request):
    return HttpResponse("contact")

@login_required(login_url='login')
@user_role(role=['admin'])
def product(request):
    product = Product.objects.all()
    context = {'products':product}
    return render(request,'account/products.html',context) 


@login_required(login_url='login')
@user_role(role=['admin'])
def customer(request,pk):
    customer = Customer.objects.get(id=pk)
    order = customer.order_set.all()
    total_order = order.count()

    myFilter = OrderFilter(request.GET,queryset=order) 
    order = myFilter.qs
    context = {'customers':customer,'orders':order,'total_order':total_order,'myFilter':myFilter}
    return render(request, 'account/customer.html',context) 


@login_required(login_url='login')
@user_role(role=['customer'])
def userProfile(request):

    order = request.user.customer.order_set.all()
    total_order = order.count()
    delivered = order.filter(status='Delevered').count()
    pending = order.filter(status='Pending').count()
    context = {'orders':order,'total_order':total_order,'delivered':delivered,'pending':pending}
    return render(request, 'account/user.html',context)


@login_required(login_url='login')
@user_role(role=['admin'])
def orderform(request,pk):
    FormSet = inlineformset_factory(Customer,Order,fields=('Product','status'),extra=5)
    customer = Customer.objects.get(id=pk)
    # form = OrderForm(initial={'customer':customer})
    form = FormSet(queryset=Order.objects.none(), instance=customer)
    if request.method == 'POST':
        form = FormSet(request.POST,instance=customer)
        if form.is_valid():
            form.save()
            return redirect('/')


    context = {'form':form}
    return render(request,'account/order_form.html',context) 


@login_required(login_url='login')
@user_role(role=['admin'])
def updateOrder(request,pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form':form,'order':order}
    return render(request,'account/order_form.html',context)


@login_required(login_url='login')
@user_role(role=['admin'])
def deleteOrder(request,pk):
    order = Order.objects.get(id=pk) 
    if request.method == 'POST':
        order.delete()
        return redirect('home')
    context = {'order':order}
    return render(request,'account/delete_order.html',context)  

@unauthenticated
def loginUser(request):
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
    context = {}
    return render(request,'account/login.html',context) 

@unauthenticated
def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            Customer.objects.create(
                user=user,
            )
            return redirect('login')    
            
    context = {'form':form}
    return render(request,'account/register.html',context)

def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@user_role(role=['customer'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()

    context = {'form':form}
    return render(request,'account/profile_settings.html',context)