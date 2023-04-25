from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect
from django.contrib import messages
import datetime
from .models import Table, Customer, Reservation
from .forms import CustomerForm, Reservations


def get_customer_instance(request, User):
    customer_email = request.user.emailcustomer = Customer.objects.filter(email=customer_email).first()
    
    return customer_email


def retrieve_reservations(self, request, User):
    if len(Customer.objects.filter(email=customer_email)) !=0:
        current_customer = Customer.objects.get(email=customer_email)
        current_customer_id = current_customer.pk
