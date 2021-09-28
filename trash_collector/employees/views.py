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
        # suspetion_dates= Customer.objects.filter(suspend_start=) 
        todays_weekly_pickup= Customer.objects.filter(weekly_pickup= today)
        todays_onetime_pickup= Customer.objects.filter(one_time_pickup= today)
        zipcode_match= Customer.objects.filter(zip_code=(Employee.zip_code))
        suspended= Customer.objects.filter(suspend_start= today) & Customer(suspend_end= today)
        


        context ={
            'logged_in_employee': logged_in_employee,
            'today': today,
            'todays_weekly_pickup': todays_weekly_pickup, 
            'todays_onetime_pickup': todays_onetime_pickup,
            'zipcode_match': zipcode_match,
            'suspended': suspended
        }
        #Customer = apps.get_model('customers.Customer')
        return render(request, 'employees/index.html')
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse(request,'employees:create', context))


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
