from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, get_object_or_404,redirect
from django.shortcuts import render
# from .models import(Holidays,Timelogs,Employees,timerequests)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect,HttpResponse
# from .models import reservations,messages

def index(request):
	return render(request,'Heart/patients.html')
