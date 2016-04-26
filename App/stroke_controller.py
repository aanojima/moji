from django.shortcuts import render, render_to_response
from django.http import *
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.conf import settings
import json, os, time

from django.core.exceptions import ObjectDoesNotExist

from App.models import *

def stroke_response(model):
	response = {
		"id" : model.id,
		"character" : {
			"id" : model.character.id,
			"character_set" : model.character.character_set,
			"name" : model.character.name
		},
		"index" : model.index
	}
	return response