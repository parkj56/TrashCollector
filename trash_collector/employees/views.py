from datetime import date
from customers.models import Customer
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from .models import Employee



# Create your views here.

# TODO: Create a function for each path created in employees/urls.py. Each will need a template as well.

@login_required
def index(request):
    # This line will get the Customer model from the other app, it can now be used to query the db for Customers
    logged_in_user = request.user
    #Customer = apps.get_model('customers.Customer')
    try:
        logged_in_employee = Employee.objects.get(user=logged_in_user)

        today = date.today()
        weekday_number= today.weekday()
        list_of_weekdays= ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        weekday= list_of_weekdays[weekday_number]
        customers_zipcode = Customer.objects.filter(zip_code = logged_in_employee.zip_code)
        # suspetion_dates= Customer.objects.filter(suspend_start=) 
        weekly_or_onetimes = customers_zipcode.filter(weekly_pickup= weekday) | customers_zipcode.filter(one_time_pickup= today)
        
        context ={
            'logged_in_employee': logged_in_employee,
            'today': today,
            'weekly_or_onetimes': weekly_or_onetimes
            
        }
      
        return render(request, 'employees/index.html', context)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('employees:create'))

@login_required
def create(request):
    logged_in_user = request.user
    if request.method == "POST":
        name_from_form = request.POST.get('name')
        zip_from_form = request.POST.get('zip_code')
        new_employee = Employee(name=name_from_form, user=logged_in_user, zip_code=zip_from_form,)
        new_employee.save()
        return HttpResponseRedirect(reverse('employees:index'))
    else:
        return render(request, 'employees/create.html')

@login_required
def edit_profile(request):
    logged_in_user = request.user
    logged_in_employee = Employee.objects.get(user=logged_in_user)
    if request.method == "POST":
        name_from_form = request.POST.get('name')
        zip_from_form = request.POST.get('zip_code')
        logged_in_employee.name = name_from_form
        logged_in_employee.zip_code = zip_from_form
        logged_in_employee.save()
        return HttpResponseRedirect(reverse( 'employees:index'))
    else:
        context = {
            'logged_in_employee': logged_in_employee
        }
        return render(request,'employees/edit_profile.html', context)

@login_required
def confirm_pickup(request, customer_id):
    Customer = apps.get_model('customers.Customer')
    customer_update = Customer.objects.get(id = customer_id)
    customer_update.balance += 20
    customer_update.save()
    return HttpResponseRedirect(reverse('employees:index'))

@login_required
def day_filter(request):
    logged_in_user = request.user
    logged_in_employee = Employee.objects.get(user=logged_in_user.pk)
    filter_customers = Customer.objects.filter(zip_code=logged_in_employee.zip_code)
    filter_day = None
    if request.method == "POST":
        filter_day = request.POST.get("filter_day") 
    context = {
        "logged_in_user": logged_in_user,
        "filter_customers": filter_customers,
        "filter_day": filter_day,
    }
    return render(request, 'employees/day_filter.html', context)