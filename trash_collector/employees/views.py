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
    try:
        logged_in_employee = Employee.objects.get(user=logged_in_user)

        today = date.today()
        weekday_number= today.weekday()
        list_of_weekdays= ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        weekday= list_of_weekdays[weekday_number]
        customers_zipcode = Customer.objects.filter(zip_code = logged_in_employee.zip_code)
        weekly_or_onetimes = customers_zipcode.filter(weekly_pickup= weekday) | customers_zipcode.filter(one_time_pickup= today)
    
        context ={
            'logged_in_employee': logged_in_employee,
            'today': today,
            'weekly_or_onetimes': weekly_or_onetimes
            
        }
        #Customer = apps.get_model('customers.Customer')
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
        return HttpResponseRedirect(reverse(request, 'employees:index'))
    else:
        context = {
            'logged_in_employee': logged_in_employee
        }
        return render(request,'employees/edit_profile.html', context)

def day_filter(request):
    logged_in_user = request.user
    logged_in_employee = Employee.objects.get(user=logged_in_user)
    if request.method == "POST":
        week_day = request.POST.get('day')
        filtered_customers = Customer.objects.filter(pickup_day=week_day)
        context = {
            'filterd_customers': filtered_customers,
            'logged_in_employee': logged_in_employee,
        }
        return render(request, 'employee:index', context)
    else:
        return render(request, 'employee:index')

@login_required
def comfirm_pickup(request, customer_id):
    customer_update = Customer.objects.get(customer_id)
    customer_update.charge += 20
    customer_update.save()
    return HttpResponseRedirect(reverse(request, 'employees:index'))

@login_required
def weekly_schedule(request):
    # This line will get the Customer model from the other app, it can now be used to query the db for Customers
    logged_in_user = request.user
    try:
        logged_in_employee = Employee.objects.get(user=logged_in_user)

        list_of_weekdays= ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        customers_zipcode = Customer.objects.filter(zip_code = logged_in_employee.zip_code)
        schedueled_pickup = customers_zipcode.filter(weekly_pickup= list_of_weekdays)
    
        context ={
            'logged_in_employee': logged_in_employee,
            'schedueled_pickup': schedueled_pickup
            
        }
        #Customer = apps.get_model('customers.Customer')
        return render(request, 'employees/index.html', context)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('employees:create'))


    