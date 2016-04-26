from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

# Create your views here.
def api(request):
	return HttpResponse("API!")