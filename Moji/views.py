from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

def splash(request):
	return render(request, 'App/splash.html', { "MOJI_URL" : settings.MOJI_URL })

def student(request):
	return render(request, 'App/student.html', { "MOJI_URL" : settings.MOJI_URL })

def teacher(request):
	return render(request, 'App/teacher.html', { "MOJI_URL" : settings.MOJI_URL })

def login(request):
	return HttpResponse("Login")

def logout(request):
	return HttpResponse("Logout")

def signup(request):
	return HttpResponse("Signup")
