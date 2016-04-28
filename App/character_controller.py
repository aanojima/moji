from django.shortcuts import render, render_to_response
from django.http import *
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.conf import settings
import json, os, time

from django.core.exceptions import ObjectDoesNotExist

from App.models import *

def character_response(model):
	response = {
		"id" : model.id,
		"name" : model.name,
		"character_set" : model.character_set,
		"points" : json.loads(model.points),
	}
	return response

@csrf_exempt
def characters(request):
	try:
		if request.method == "GET":
			# GET MANY
			response_data = { "characters" : [] }
			characters = Character.objects.all()
			for character in characters:
				response_data["characters"].append(character_response(character))
			return HttpResponse(json.dumps(response_data), content_type="application/json")
		elif request.method == "POST":
			# NEW Character
			character_model = Character(name=request.POST.get("name"), character_set=request.POST.get("character_set"))
			character_model.save()
			response_data = {
				"character" : character_response(character_model),
				"success" : True
			}
			return HttpResponse(json.dumps(response_data), content_type="application/json")
		else:
			return HttpResponseNotAllowed(['GET', 'POST'])
	except Exception, e:
		# TODO: Error-Handling
		raise

@csrf_exempt
def character(request, character_id):
	try:
		if request.method == "GET":
			# GET - READ
			try:
				character = Character.objects.get(id=character_id)
				response_data = {
					"character" : character_response(character)
				}
				return HttpResponse(json.dumps(response_data), content_type="application/json")
			except ObjectDoesNotExist:
				return HttpResponse(status=404)
		elif request.method == "PUT":
			# PUT - UPDATE - later
			data = json.loads(request.body)
			try:
				character = Character.objects.get(
					name=data["character"]["character-name"],
					character_set=data["character"]["character-set"])
			except ObjectDoesNotExist:
				character = Character(
					name=data["character"]["character-name"],
					character_set=data["character"]["character-set"])
				character.save()
			character.points = json.dumps(data["strokes"])
			character.save()
		elif request.method == "DELETE":
			character = Character.objects.get(id=character_id)
			character.delete()
			response_data = { "success" : True }
			return HttpResponse(json.dumps(response_data), content_type="application/json")
		else:
			return HttpResponseNotAllowed(['GET', 'PUT', 'DELETE'])
		return HttpResponse("API call for character #" + character_id)
	except ObjectDoesNotExist:
		return HttpResponse(status=404)
	except Exception, e:
		# TODO: Error-Handling
		raise

	# try:
	# 	character = Character.objects.get(id=character_id)
	# 	if character.points == '':
	# 		# Points not yet defined
	# 		return 0
	# 	points = json.loads(character.points)
	# 	if points is not None:
	# except ObjectDoesNotExist:
	# 	return -1