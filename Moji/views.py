from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

def home(request):
	return render(request, 'App/home.html', {})

def login(request):
	return HttpResponse("Login")

def logout(request):
	return HttpResponse("Logout")

def signup(request):
	return HttpResponse("Signup")