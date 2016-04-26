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

def get_stroke_count(character_id):
	try:
		character = Character.objects.get(id=character_id)
		if character.points == '':
			# Points not yet defined
			return 0
		points = json.loads(character.points)
		if points is not None:
			return len(points)
		return 0
	except ObjectDoesNotExist:
		return -1

def get_endpoints(character_id):
	try:
		character = Character.objects.get(id=character_id)
		if character.points == '':
			# Points not yet defined
			return []
		points = json.loads(character.points)
		if points is not None:
			endpoints = []
			for i in range(len(points)):
				stroke = points[i]
				start = stroke[0]
				end = stroke[len(stroke) - 1]
				strokeEndpoints = [
					[start[0], start[1]],
					[end[0], end[1]]
				]
				endpoints.append(strokeEndpoints)
			return endpoints
		return []
	except ObjectDoesNotExist:
		return None

def calculate_COG(character_id):
	try:
		character = Character.objects.get(id=character_id)
		if character.points == '':
			# Points not yet defined
			return [0,0]
		points = json.loads(character.points)
		if points is not None:
			num_points = 0
			total_x = 0
			total_y = 0
			for i in range(len(points)):
				stroke = points[i]
				num_points += len(stroke)
				for j in range(len(stroke)):
					point = stroke[j]
					total_x += point[0]
					total_y += point[1]
			return [float(total_x) / num_points, float(total_y) / num_points]
		return [0,0]
	except ObjectDoesNotExist:
		return [-1, -1]

def calculate_stroke_COGs(character_id):
	try:
		character = Character.objects.get(id=character_id)
		if character.points == '':
			# Points not yet defined
			return []
		points = json.loads(character.points)
		if points is not None:
			stroke_COGs = []
			for i in range(len(points)):
				stroke = points[i]
				num_points = 0
				total_x = 0
				total_y = 0
				num_points = len(stroke)
				for j in range(len(stroke)):
					point = stroke[j]
					total_x += point[0]
					total_y += point[1]
				COG = [float(total_x) / num_points, float(total_y) / num_points]
				stroke_COGs.append(COG)
			return stroke_COGs
		return []
	except ObjectDoesNotExist:
		return None

def calculate_derivatives(character_id):
	try:
		character = Character.objects.get(id=character_id)
		if character.points == '':
			# Points not yet defined
			return []
		points = json.loads(character.points)
		if points is not None:
			derivatives = []
			for i in range(len(points)):
				stroke_derivatives = []
				stroke = points[i]
				for j in range(len(stroke)):
					point = stroke[j]
					dx = 0
					dy = 0
					if j == 0:
						# FIRST
						next_point = stroke[j+1]
						dx = next_point[0] - point[0]
						dy = next_point[1] - point[1]
					elif j == len(stroke) - 1:
						# LAST
						prev_point = stroke[j-1]
						dx = point[0] - prev_point[0]
						dy = point[1] - prev_point[1]
					else:
						# INBETWEEN
						prev_point = stroke[j-1]
						next_point = stroke[j+1]
						dx = 0.5 * (next_point[0] - prev_point[0])
						dy = 0.5 * (next_point[1] - prev_point[1])
					if dx == 0:
						dx = 0.001
					if dy == 0:
						dy = 0.001
					point_derivative = [dx, dy]
					stroke_derivatives.append(point_derivative)
				derivatives.append(stroke_derivatives)
			return derivatives
		return []
	except ObjectDoesNotExist:
		return None

def get_line_segments(character_id):
	try:
		character = Character.objects.get(id=character_id)
		if character.points == '':
			# Points not yet defined
			return []
		points = json.loads(character.points)
		if points is not None:
			line_segments = []
			for i in range(len(points)):
				stroke = points[i]
				for j in range(len(stroke)):
					point = stroke[j]
					if j < len(stroke) - 1:
						# Not the last point
						next_point = stroke[j + 1]
						if point[0] <= next_point[0]:
							left = point
							right = next_point
						else:
							left = next_point
							right = point
						line_segment = {
							"stroke" : i,
							"segment" : j,
							"left" : left,
							"right" : right
						}
						line_segments.append(line_segment)
			return line_segments
		return []
	except ObjectDoesNotExist:
		return None

def calculate_stroke_ranges(character_id):
	try:
		character = Character.objects.get(id=character_id)
		if character.points == '':
			# Points not yet defined
			return []
		points = json.loads(character.points)
		if points is not None:
			stroke_ranges = []
			for i in range(len(points)):
				stroke = points[i]
				x_min = float('inf')
				y_min = float('inf')
				x_max = float('inf')*-1
				y_max = float('inf')*-1
				for j in range(len(stroke)):
					point = stroke[j]
					x_min = min(x_min, point[0])
					y_min = min(y_min, point[1])
					x_max = max(x_max, point[0])
					y_max = max(y_max, point[1])
				stroke_range = [x_min, y_min, x_max, y_max]
				stroke_ranges.append(stroke_range)
			return stroke_ranges
		return []
	except ObjectDoesNotExist:
		return None

def calculate_range(character_id):
	try:
		character = Character.objects.get(id=character_id)
		if character.points == '':
			# Points not yet defined
			return []
		points = json.loads(character.points)
		if points is not None:
			stroke_ranges = calculate_stroke_ranges(character_id)
			x_min = float('inf')
			y_min = float('inf')
			x_max = float('inf')*-1
			y_max = float('inf')*-1
			for i in range(len(stroke_ranges)):
				rng = stroke_ranges[i]
				x_min = min(x_min, rng[0])
				y_min = min(y_min, rng[1])
				x_max = max(x_max, rng[2])
				y_max = max(y_max, rng[3])
			return [x_min, y_min, x_max, y_max]
		return []
	except ObjectDoesNotExist:
		return None

def calculate_line_segment_intersections(lineA, lineB):
	alx = lineA["left"][0]
	arx = lineA["right"][0]
	aly = lineA["left"][1]
	ary = lineA["right"][1]
	blx = lineB["left"][0]
	brx = lineB["right"][0]
	bly = lineB["left"][1]
	bry = lineB["right"][1]

	sax = arx - alx
	say = ary - aly
	sbx = brx - blx
	sby = bry - bly

	d = -1*sbx * say + sax * sby
	if d == 0:
		return None

	s = float(-1*say * (alx - brx) + sax * (aly - bry)) / d
	t = float(   sbx * (aly - bry) - sby * (alx - brx)) / d

	if lineA["stroke"] == lineB["stroke"]:
		if s > 0 and s < 1 and t > 0 and t < 1:
			# Collision detected
			ix = alx + (t * sax)
			iy = aly + (t * say)
			intersection = {
				"point" : [ix, iy],
				"strokeA" : lineA["stroke"],
				"strokeB" : lineB["stroke"]
			}
			return intersection
	else:
		if s >= 0 and s <= 1 and t >= 0 and t <= 1:
			# Collision detected
			ix = alx + (t * sax)
			iy = aly + (t * say)
			intersection = {
				"point" : [ix, iy],
				"strokeA" : lineA["stroke"],
				"strokeB" : lineB["stroke"]
			}
			return intersection

	return None

def calculate_intersections(character_id):
	try:
		character = Character.objects.get(id=character_id)
		if character.points == '':
			# Points not yet defined
			return []
		points = json.loads(character.points)
		if points is not None:
			# TODO: Using AVL Tree and Line Sweep Method
			intersections = {
				"multiple" : [],
				"single" : []
			}
			line_segments = get_line_segments(character_id)
			for i in range(len(line_segments)):
				lineA = line_segments[i]
				for j in range(i+1, len(line_segments)):
					lineB = line_segments[j]
					intersection = calculate_line_segment_intersections(lineA, lineB)
					if intersection is not None:
						if lineA["stroke"] == lineB["stroke"]:
							lastIndex = len(intersections["single"]) - 1
							if lastIndex == -1:
								intersections["single"].append(intersection)
								continue
							lastIntersection = intersections["single"][lastIndex]
							p0 = lastIntersection["point"]
							p1 = intersection["point"]
							import math
							d = math.sqrt(math.pow(p1[0]-p0[0],2)+math.pow(p1[1]-p0[1],2))
							if d > 5:
								intersections["single"].append(intersection)
						else:
							lastIndex = len(intersections["multiple"]) - 1
							if lastIndex == -1:
								intersections["multiple"].append(intersection)
								continue
							lastIntersection = intersections["multiple"][lastIndex]
							p0 = lastIntersection["point"]
							p1 = intersection["point"]
							import math
							d = math.sqrt(math.pow(p1[0]-p0[0],2)+math.pow(p1[1]-p0[1],2))
							if d > 5:
								intersections["multiple"].append(intersection)
			return intersections
		return []
	except ObjectDoesNotExist:
		return None