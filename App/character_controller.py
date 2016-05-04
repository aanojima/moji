from django.shortcuts import render, render_to_response
from django.http import *
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.conf import settings
import json, os, time, unicodedata

from django.core.exceptions import ObjectDoesNotExist

from App.models import *
from App.unicode_blocks import *

def character_response(model):
	response = {
		"unicode-value" : model.unicode_value,
		"unicode-block" : model.unicode_block,
		"unicode-description" : model.unicode_description,
		# "points" : json.loads(model.points),
	}
	return response

@csrf_exempt
def characters(request):
	try:
		if request.method == "GET":
			# GET MANY
			response_data = { "characters" : [] }
			characters = Character.objects.all().order_by("unicode_value")
			for character in characters:
				response_data["characters"].append(character_response(character))
			return HttpResponse(json.dumps(response_data), content_type="application/json")
		elif request.method == "POST":
			# NEW Character
			unicode_display = request.POST.get("unicode-display")
			unicode_value = ord(unicode_display) # Opposite of unichr
			unicode_block = get_block_of(unicode_display)
			unicode_description = unicodedata.name(unicode_display)
			try:
				Character.objects.get(unicode_value=unicode_value)
				return HttpResponseBadRequest("Unicode character already exists")
			except ObjectDoesNotExist:
				character_model = Character(
					unicode_value=unicode_value,
					unicode_block=unicode_block,
					unicode_description=unicode_description)
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
def character(request, unicode_value):
	try:
		if request.method == "GET":
			# GET - READ
			try:
				character = Character.objects.get(unicode_value=unicode_value)
				response_data = {
					"character" : character_response(character)
				}
				return HttpResponse(json.dumps(response_data), content_type="application/json")
			except ObjectDoesNotExist:
				return HttpResponse(status=404)
		elif request.method == "PUT":
			# PUT - UPDATE
			data = json.loads(request.body) # Opposite of unichr
			unicode_display = unichr(int(unicode_value))
			unicode_block = get_block_of(unicode_display)
			unicode_description = unicodedata.name(unicode_display)
			try:
				character = Character.objects.get(unicode_value=unicode_value)
			except ObjectDoesNotExist:
				character = Character(
					unicode_value=unicode_value,
					unicode_block=unicode_block,
					unicode_description=unicode_description)
				character.save()
			character.points = json.dumps(data["strokes"])
			character.save()
		elif request.method == "DELETE":
			character = Character.objects.get(id=unicode_value)
			character.delete()
			response_data = { "success" : True }
			return HttpResponse(json.dumps(response_data), content_type="application/json")
		else:
			return HttpResponseNotAllowed(['GET', 'PUT', 'DELETE'])
		return HttpResponse("API call for character #" + unicode_value)
	except ObjectDoesNotExist:
		return HttpResponse(status=404)
	except Exception, e:
		# TODO: Error-Handling
		raise

	# try:
	# 	character = Character.objects.get(id=unicode_value)
	# 	if character.points == '':
	# 		# Points not yet defined
	# 		return 0
	# 	points = json.loads(character.points)
	# 	if points is not None:
	# except ObjectDoesNotExist:
	# 	return -1

@csrf_exempt
def character_blocks(request):
	try:
		if request.method == "GET":
			# GET MANY
			unicode_block = request.GET.get('unicode_block')
			if unicode_block is not None:
				response_data = { "characters" : [] }
				characters = Character.objects.filter(unicode_block=unicode_block).order_by('unicode_value')
				for character in characters:
					response_data["characters"].append(character_response(character))
				return HttpResponse(json.dumps(response_data), content_type="application/json")
			response_data = { "blocks" : {} }
			characters = Character.objects.all().order_by("unicode_value")
			for character in characters:
				block = character.unicode_block
				if response_data["blocks"].has_key(block):
					response_data["blocks"][block] += 1
				else:
					response_data["blocks"][block] = 1
			return HttpResponse(json.dumps(response_data), content_type="application/json")
		else:
			return HttpResponseNotAllowed(['GET'])
	except Exception, e:
		# TODO: Error-Handling
		raise