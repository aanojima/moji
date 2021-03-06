from django.shortcuts import render, render_to_response
from django.http import *
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.conf import settings
from decimal import Decimal
import json, os, time, math

from django.core.exceptions import ObjectDoesNotExist

from App.models import *
import App.grader

def grade_character_by_ratio(value, params, result, label, small_feedback, large_feedback):
	SMALL_ALLOWANCE = params["small-allowance"] # -0.1
	SMALL_LIMIT = params["small-limit"] # -0.5
	LARGE_ALLOWANCE = params["large-allowance"] # 0.20
	LARGE_LIMIT = params["large-limit"] # 1.0
	if value > SMALL_ALLOWANCE and value < LARGE_ALLOWANCE:
		# Allowable
		a = 0
		b = 1
		c = 0
	elif value < SMALL_ALLOWANCE:
		# smaller ratio
		a = max(value, SMALL_LIMIT) - SMALL_ALLOWANCE
		b = SMALL_LIMIT - SMALL_ALLOWANCE
		c = -1
	elif value > LARGE_ALLOWANCE:
		# greater ratio
		a = min(value, LARGE_LIMIT) - LARGE_ALLOWANCE
		b = LARGE_LIMIT - LARGE_ALLOWANCE
		c = 1
	else:
		a = 1
		b = 1
		c = None
	score = 1 - (a / b)
	feedback_type = c
	if type(result["character-grade-data"][label]) == type([]):
		result["character-grade-data"][label].append(score)
	else:
		result["character-grade-data"][label] = score
	if feedback_type is not None:
		if feedback_type == 0:
			feedback = "Acceptable"
		elif feedback_type == 1:
			feedback = large_feedback
		elif feedback_type == -1:
			feedback = small_feedback
		else:
			feedback = "Unhandled"
	if type(result["character-grade-data"][label]) == type([]):
		result["character-feedback"][label].append(feedback)
	else:
		result["character-feedback"][label] = feedback

def grade_stroke_by_ratio(value, params, result, label, small_feedback, large_feedback):
	SMALL_ALLOWANCE = params["small-allowance"] # -0.1
	SMALL_LIMIT = params["small-limit"] # -0.5
	LARGE_ALLOWANCE = params["large-allowance"] # 0.20
	LARGE_LIMIT = params["large-limit"] # 1.0
	if value > SMALL_ALLOWANCE and value < LARGE_ALLOWANCE:
		# Allowable
		a = 0
		b = 1
		c = 0
	elif value < SMALL_ALLOWANCE:
		# smaller ratio
		a = max(value, SMALL_LIMIT) - SMALL_ALLOWANCE
		b = SMALL_LIMIT - SMALL_ALLOWANCE
		c = -1
	elif value > LARGE_ALLOWANCE:
		# greater ratio
		a = min(value, LARGE_LIMIT) - LARGE_ALLOWANCE
		b = LARGE_LIMIT - LARGE_ALLOWANCE
		c = 1
	else:
		a = 1
		b = 1
		c = None
	score = 1 - (a / b)
	feedback_type = c
	if type(result["strokes-grade-data"][label]) == type([]):
		result["strokes-grade-data"][label].append(score)
	else:
		result["strokes-grade-data"][label] = score
	if feedback_type is not None:
		if feedback_type == 0:
			feedback = "Acceptable"
		elif feedback_type == 1:
			feedback = large_feedback
		elif feedback_type == -1:
			feedback = small_feedback
		else:
			feedback = "Unhandled"
	if type(result["strokes-grade-data"][label]) == type([]):
		result["strokes-feedback"][label].append(feedback)
	else:
		result["strokes-feedback"][label] = feedback

def score(grades, weights):
	total = 0
	weight = 0
	for key in grades:
		if type(grades[key]) == type([]):
			num = len(grades[key])
			if num == 0:
				continue
			subgrade = 0
			for grade in grades[key]:
				subgrade += grade
			subgrade /= float(num)
			weight += weights[key]
			total += subgrade * weights[key]
		else:
			weight += weights[key]
			total += grades[key] *  weights[key]
	return total / float(weight)

def evaluate(expected_points, submitted_points):
	# Return grade/feedback by comparing certain statistics
	# generated by methods that take the stroke points as a parameter

	# GRADING POLICY
	#
	# Character Grade: 30%
	# - Stroke Count: 50% (all or nothing) DONE
	# - Dimension Ratio: 50% DONE
	# - Number of Cross Intersections: 10% DONE
	# - Relative Location of Cross Intersections: 10% (wrt two stroke ranges -> TODO)
	#
	#
	# Strokes Grade: 70% (Following Grades per Stroke)
	# - Dimensions: 10% (DONE)
	# - Number of Self Intersections: 10%% (TODO)
	# - Relative Location of Self Intersections: 10% (wrt stroke range) (TODO)
	# - Relative Location of Stroke Range: 10% - 20% (wrt character range) (TODO)
	# - Relative Location of Endpoints: 10% (wrt stroke range) (TODO)
	# - Stroke Shape (Using Positions and Derivatives): 30% - 40% TODO: Difficult

	# TODO: PUT ALL SCORING WEIGHTS AS CONSTANTS AND PUT IN RESULT
	GRADE_WEIGHTS = {
		"character" : 0.30,
		"strokes" : 0.70
	}

	CHARACTER_DIMENSION_RATIO = "character-dimension-ratio"
	CHARACTER_STROKE_COUNT = "character-stroke-count"
	CHARACTER_CROSS_INTERSECTIONS = "character-cross-intersections"
	CHARACTER_CROSS_INTERSECTIONS_X = "character-cross-intersections-x"
	CHARACTER_CROSS_INTERSECTIONS_Y = "character-cross-intersections-y"
	CHARACTER_GRADE_WEIGHTS = {
		CHARACTER_DIMENSION_RATIO : 0.3,
		CHARACTER_STROKE_COUNT : 0.2,
		CHARACTER_CROSS_INTERSECTIONS : 0.3,
		CHARACTER_CROSS_INTERSECTIONS_X : 0.1,
		CHARACTER_CROSS_INTERSECTIONS_Y : 0.1
	}
	CHARACTER_GRADE_DATA = {
		CHARACTER_DIMENSION_RATIO : 0,
		CHARACTER_STROKE_COUNT : 0,
		CHARACTER_CROSS_INTERSECTIONS : 0,
		CHARACTER_CROSS_INTERSECTIONS_X : [],
		CHARACTER_CROSS_INTERSECTIONS_Y : []
	}
	CHARACTER_FEEDBACK = {
		CHARACTER_DIMENSION_RATIO : None,
		CHARACTER_STROKE_COUNT : None,
		CHARACTER_CROSS_INTERSECTIONS : None,
		CHARACTER_CROSS_INTERSECTIONS_X : [],
		CHARACTER_CROSS_INTERSECTIONS_Y : []
	}

	for key in CHARACTER_GRADE_DATA:
		if type(CHARACTER_GRADE_DATA[key]) == type([]):
			# sum
			continue
		else:
			# Weight * Grade
			continue

	STROKE_WIDTH = "stroke-width"
	STROKE_HEIGHT = "stroke-height"
	STROKE_SELF_INTERSECTIONS = "stroke-self-intersections"
	STROKE_SELF_INTERSECTIONS_X = "stroke-self-intersections-x"
	STROKE_SELF_INTERSECTIONS_Y = "stroke-self-intersections-y"
	STROKE_RANGE_LOCATION_X = "stroke-range-location-x"
	STROKE_RANGE_LOCATION_Y = "stroke-range-location-y"
	STROKE_STARTPOINT_LOCATION_X = "stroke-startpoint-location-x"
	STROKE_STARTPOINT_LOCATION_Y = "stroke-startpoint-location-y"
	STROKE_ENDPOINT_LOCATION_X = "stroke-endpoint-location-x"
	STROKE_ENDPOINT_LOCATION_Y = "stroke-endpoint-location-y"
	STROKE_SHAPE = "stroke-shape"
	STROKE_GRADE_WEIGHTS = {
		STROKE_WIDTH : 0.05,
		STROKE_HEIGHT : 0.05,
		STROKE_SELF_INTERSECTIONS : 0.1,
		STROKE_SELF_INTERSECTIONS_X : 0.05,
		STROKE_SELF_INTERSECTIONS_Y : 0.05,
		STROKE_RANGE_LOCATION_X : 0.05,
		STROKE_RANGE_LOCATION_Y : 0.05,
		STROKE_STARTPOINT_LOCATION_X : 0.025,
		STROKE_STARTPOINT_LOCATION_Y : 0.025,
		STROKE_ENDPOINT_LOCATION_X : 0.025,
		STROKE_ENDPOINT_LOCATION_Y : 0.025,
		STROKE_SHAPE : 0.5
	}
	STROKE_GRADE_DATA = {
		STROKE_WIDTH : [],
		STROKE_HEIGHT : [],
		STROKE_SELF_INTERSECTIONS : 0,
		STROKE_SELF_INTERSECTIONS_X : [],
		STROKE_SELF_INTERSECTIONS_Y : [],
		STROKE_RANGE_LOCATION_X : [],
		STROKE_RANGE_LOCATION_Y : [],
		STROKE_STARTPOINT_LOCATION_X : [],
		STROKE_STARTPOINT_LOCATION_Y : [],
		STROKE_ENDPOINT_LOCATION_X : [],
		STROKE_ENDPOINT_LOCATION_Y : [],
		STROKE_SHAPE : []
	}
	STROKE_FEEDBACK = {
		STROKE_WIDTH : [],
		STROKE_HEIGHT : [],
		STROKE_SELF_INTERSECTIONS : None,
		STROKE_SELF_INTERSECTIONS_X : [],
		STROKE_SELF_INTERSECTIONS_Y : [],
		STROKE_RANGE_LOCATION_X : [],
		STROKE_RANGE_LOCATION_Y : [],
		STROKE_STARTPOINT_LOCATION_X : [],
		STROKE_STARTPOINT_LOCATION_Y : [],
		STROKE_ENDPOINT_LOCATION_X : [],
		STROKE_ENDPOINT_LOCATION_Y : [],
		STROKE_SHAPE : []
	}

	RATIO_PARAMS = {
		"small-allowance" : -0.15,
		"small-limit" : -0.5,
		"large-allowance" : 0.3,
		"large-limit" : 1.0
	}

	DIFFERENCE_PARAMS = {
		"small-allowance" : -0.1,
		"small-limit" : -0.5,
		"large-allowance" : 0.1,
		"large-limit" : 0.5
	}

	result = {
		# "data" : {},
		"overall-grade" : 0.0,
		"character-grade" : 0.0,
		# "character-grade-weights" : CHARACTER_GRADE_WEIGHTS,
		"character-grade-data" : CHARACTER_GRADE_DATA,
		"character-feedback" : CHARACTER_FEEDBACK,
		"strokes-grade" : 0.0,
		"strokes-grade-data" : STROKE_GRADE_DATA,
		# "strokes-grade-weights" : STROKE_GRADE_WEIGHTS,
		"strokes-feedback" : STROKE_FEEDBACK
	}


	# CHARACTER and STROKES Expected and Submitted Data
	expected_stroke_count = grader.get_stroke_count(expected_points)
	submitted_stroke_count = grader.get_stroke_count(submitted_points)
	expected_range = grader.calculate_range(expected_points)
	submitted_range = grader.calculate_range(submitted_points)
	[expected_x_min, expected_y_min, expected_x_max, expected_y_max] = expected_range
	[submitted_x_min, submitted_y_min, submitted_x_max, submitted_y_max] = submitted_range
	expected_width = expected_x_max - expected_x_min
	submitted_width = submitted_x_max - submitted_x_min
	expected_height = expected_y_max - expected_y_min
	submitted_height = submitted_y_max - submitted_y_min
	expected_stroke_ranges = grader.calculate_stroke_ranges(expected_points)
	submitted_stroke_ranges = grader.calculate_stroke_ranges(submitted_points)
	expected_endpoints = grader.get_endpoints(expected_points)
	submitted_endpoints = grader.get_endpoints(submitted_points)
	expected_intersections = grader.calculate_intersections(expected_points)
	submitted_intersections = grader.calculate_intersections(submitted_points)
	expected_derivatives = grader.calculate_derivatives(expected_points)
	submitted_derivatives = grader.calculate_derivatives(submitted_points)
	STROKE_SHAPE_SCORE_TOLERANCE = 0.85
	STROKE_SHAPE_SCORE_LIMIT = 0.5

	# CHARACTER Stroke Count
	result["character-feedback"][CHARACTER_STROKE_COUNT] = submitted_stroke_count - expected_stroke_count
	if expected_stroke_count != submitted_stroke_count:
		result["character-grade-data"][CHARACTER_STROKE_COUNT] = 0
		return result
	else:
		result["character-grade-data"][CHARACTER_STROKE_COUNT] = 1

	# CHARACTER Dimension Ratio
	expected_ratio = expected_width / float(expected_height)
	submitted_ratio = submitted_width / float(submitted_height)
	value = (submitted_ratio / expected_ratio) - 1.0 # 0.5-2.0
	grade_character_by_ratio(value, RATIO_PARAMS, 
		result, CHARACTER_DIMENSION_RATIO, "Long / Narrow", "Wide / Short")

	# CHARACTER Cross-Intersections
	num_expected_multi_intersections = len(expected_intersections["multiple"])
	num_submitted_multi_intersections = len(submitted_intersections["multiple"])
	result["character-feedback"][CHARACTER_CROSS_INTERSECTIONS] = num_submitted_multi_intersections - num_expected_multi_intersections
	if num_expected_multi_intersections == num_submitted_multi_intersections:
		result["character-grade-data"][CHARACTER_CROSS_INTERSECTIONS] = 1
		# CHARAACTER Cross-Intersections Locations (X,Y)
		n_mi = len(expected_intersections["multiple"])
		for i in range(n_mi):
			e_m_intersection = expected_intersections["multiple"][i]
			s_m_intersection = submitted_intersections["multiple"][i]
			[emix, emiy] = e_m_intersection["point"]
			[smix, smiy] = s_m_intersection["point"]
			expected_strokeA = e_m_intersection["segmentA"]["stroke"]
			[eA_xmin, eA_ymin, eA_xmax, eA_ymax] = expected_stroke_ranges[expected_strokeA]
			expected_strokeB = e_m_intersection["segmentB"]["stroke"]
			[eB_xmin, eB_ymin, eB_xmax, eB_ymax] = expected_stroke_ranges[expected_strokeB]
			submitted_strokeA = s_m_intersection["segmentA"]["stroke"]
			[sA_xmin, sA_ymin, sA_xmax, sA_ymax] = submitted_stroke_ranges[submitted_strokeA]
			submitted_strokeB = s_m_intersection["segmentB"]["stroke"]
			[sB_xmin, sB_ymin, sB_xmax, sB_ymax] = submitted_stroke_ranges[submitted_strokeB]
			e_strokeA_width = eA_xmax - eA_xmin
			e_strokeA_height = eA_ymax - eA_ymin
			e_strokeB_width = eB_xmax - eB_xmin
			e_strokeB_height = eB_ymax - eB_ymin
			e_max_stroke_width = max(e_strokeA_width, e_strokeB_width)
			if e_strokeA_width == e_max_stroke_width:
				e_xmin = eA_xmin
			else:
				e_xmin = eB_xmin
			e_max_stroke_height = max(e_strokeA_height, e_strokeB_height)
			if e_strokeA_height == e_max_stroke_height:
				e_ymin = eA_ymin
			else:
				e_ymin = eB_ymin
			s_strokeA_width = eA_xmax - eA_xmin
			s_strokeA_height = eA_ymax - eA_ymin
			s_strokeB_width = eB_xmax - eB_xmin
			s_strokeB_height = eB_ymax - eB_ymin
			s_max_stroke_width = max(s_strokeA_width, s_strokeB_width)
			if s_strokeA_width == s_max_stroke_width:
				s_xmin = eA_xmin
			else:
				s_xmin = eB_xmin
			s_max_stroke_height = max(s_strokeA_height, s_strokeB_height)
			if s_strokeA_height == s_max_stroke_height:
				s_ymin = eA_ymin
			else:
				s_ymin = eB_ymin
			emix_ratio = (emix - e_xmin) / e_max_stroke_width
			emiy_ratio = (emiy - e_ymin) / e_max_stroke_height
			smix_ratio = (smix - s_xmin) / s_max_stroke_width
			smiy_ratio = (smiy - s_ymin) / s_max_stroke_height
			mix_value = smix_ratio - emix_ratio
			miy_value = smiy_ratio - emiy_ratio
			grade_character_by_ratio(mix_value, DIFFERENCE_PARAMS,
				result, CHARACTER_CROSS_INTERSECTIONS_X, "Left", "Right")
			grade_character_by_ratio(miy_value, DIFFERENCE_PARAMS,
				result, CHARACTER_CROSS_INTERSECTIONS_Y, "High", "Low")

	# STROKES Self-Intersections
	num_expected_self_intersections = len(expected_intersections["single"])
	num_submitted_self_intersections = len(submitted_intersections["single"])
	print num_expected_self_intersections, num_submitted_self_intersections
	result["strokes-feedback"][STROKE_SELF_INTERSECTIONS] = num_submitted_self_intersections - num_expected_self_intersections
	if num_expected_self_intersections == num_submitted_self_intersections:
		result["strokes-grade-data"][STROKE_SELF_INTERSECTIONS] = 1
		# STROKES Self-Intersections Locations (X,Y)
		n_si = len(expected_intersections["single"])
		for i in range(n_si):
			e_s_intersection = expected_intersections["single"][i]
			s_s_intersection = submitted_intersections["single"][i]
			[esix, esiy] = e_s_intersection["point"]
			[ssix, ssiy] = s_s_intersection["point"]
			expected_stroke = e_s_intersection["segmentA"]["stroke"]
			[e_xmin, e_ymin, e_xmax, e_ymax] = expected_stroke_ranges[expected_stroke]
			submitted_stroke = s_s_intersection["segmentA"]["stroke"]
			[s_xmin, s_ymin, s_xmax, s_ymax] = submitted_stroke_ranges[submitted_stroke]
			e_stroke_width = e_xmax - e_xmin
			e_stroke_height = e_ymax - e_ymin
			s_stroke_width = s_xmax - s_xmin
			s_stroke_height = s_ymax - s_ymin
			esix_ratio = (esix - e_xmin) / e_stroke_width
			esiy_ratio = (esiy - e_ymin) / e_stroke_height
			ssix_ratio = (ssix - s_xmin) / s_stroke_width
			ssiy_ratio = (ssiy - s_ymin) / s_stroke_height
			six_value = ssix_ratio - esix_ratio
			siy_value = ssiy_ratio - esiy_ratio
			grade_stroke_by_ratio(six_value, DIFFERENCE_PARAMS,
				result, STROKE_SELF_INTERSECTIONS_X, "Left", "Right")
			grade_stroke_by_ratio(siy_value, DIFFERENCE_PARAMS,
				result, STROKE_SELF_INTERSECTIONS_Y, "High", "Low")

	# STROKES
	for i in range(expected_stroke_count):
		# STROKES Expected and Submitted Data
		expected_stroke = expected_points[i]
		submitted_stroke = submitted_points[i]
		expected_stroke_range = expected_stroke_ranges[i]
		submitted_stroke_range = submitted_stroke_ranges[i]
		[exmin, eymin, exmax, eymax] = expected_stroke_range
		[sxmin, symin, sxmax, symax] = submitted_stroke_range
		es_width = exmax - exmin
		es_height = eymax - eymin
		ss_width = sxmax - sxmin
		ss_height = symax - symin
		[[espx, espy], [eepx, eepy]] = expected_endpoints[i]
		[[sspx, sspy], [sepx, sepy]] = submitted_endpoints[i]
		MAX_TOLERANCE = 0.5
		MIN_TOLERANCE = 0.1
		expected_stroke_derivatives = expected_derivatives[i]
		submitted_stroke_derivatives = submitted_derivatives[i]

		# STROKES Width and Height
		ewidth = (exmax - exmin) / float(expected_width)
		swidth = (sxmax - sxmin) / float(submitted_width)
		eheight = (eymax - eymin) / float(expected_height)
		sheight = (symax - symin) / float(submitted_height)
		width_ratio = swidth - ewidth
		stroke_dimension_params = {
			"small-allowance" : -0.15,
			"small-limit" : -0.5,
			"large-allowance" : 0.15,
			"large-limit" : 0.5
		}
		grade_stroke_by_ratio(width_ratio, stroke_dimension_params,
			result, STROKE_WIDTH, "Narrow", "Wide")
		height_ratio = sheight - eheight
		grade_stroke_by_ratio(height_ratio, stroke_dimension_params,
			result, STROKE_HEIGHT, "Short", "Long")
		
		# STROKES Range Location (X,Y)
		expected_stroke_range_x_mid = 0.5 * (exmin + exmax)
		expected_stroke_range_y_mid = 0.5 * (eymin + eymax)
		submitted_stroke_range_x_mid = 0.5 * (sxmin + sxmax)
		submitted_stroke_range_y_mid = 0.5 * (symin + symax)
		expected_stroke_range_x_ratio = (expected_stroke_range_x_mid - expected_x_min) / expected_width
		expected_stroke_range_y_ratio = (expected_stroke_range_y_mid - expected_y_min) / expected_height
		submitted_stroke_range_x_ratio = (submitted_stroke_range_x_mid - submitted_x_min) / submitted_width
		submitted_stroke_range_y_ratio = (submitted_stroke_range_y_mid - submitted_y_min) / submitted_height
		stroke_range_x_offset = submitted_stroke_range_x_ratio - expected_stroke_range_x_ratio
		stroke_range_y_offset = submitted_stroke_range_y_ratio - expected_stroke_range_y_ratio
		range_params = {
			"small-allowance" : -0.10,
			"small-limit" : -0.5,
			"large-allowance" : 0.10,
			"large-limit" : 0.5
		}
		grade_stroke_by_ratio(stroke_range_x_offset, range_params,
			result, STROKE_RANGE_LOCATION_X, "Left", "Right")
		grade_stroke_by_ratio(stroke_range_y_offset, range_params,
			result, STROKE_RANGE_LOCATION_Y, "High", "Low")


		# STROKES Startpoints (X,Y)
		espx_ratio = (espx - expected_x_min) / float(expected_width)
		espy_ratio = (espy - expected_y_min) / float(expected_height)
		sspx_ratio = (sspx - submitted_x_min) / float(submitted_width)
		sspy_ratio = (sspy - submitted_y_min) / float(submitted_height)
		if espx_ratio == 0:
			# only allow halfway
			if sspx_ratio < MIN_TOLERANCE:
				spx_score = 1.0
				spx_feedback = "Acceptable"
			else:
				spx_score = 1 - (min(sspx_ratio, MAX_TOLERANCE) - MIN_TOLERANCE) / (MAX_TOLERANCE - MIN_TOLERANCE)
				spx_feedback = "Right"
			result["strokes-grade-data"][STROKE_STARTPOINT_LOCATION_X].append(spx_score)
			result["strokes-feedback"][STROKE_STARTPOINT_LOCATION_X].append(spx_feedback)
		else:
			spx_ratio_offset = sspx_ratio - espx_ratio
			grade_stroke_by_ratio(spx_ratio_offset, DIFFERENCE_PARAMS,
				result, STROKE_STARTPOINT_LOCATION_X, "Left", "Right")
		if espy_ratio == 0:
			# only allow halfway
			if sspy_ratio < MIN_TOLERANCE:
				spy_score = 1.0
				spy_feedback = "Acceptable"
			else:
				spy_score = 1 - (min(sspy_ratio, MAX_TOLERANCE) - MIN_TOLERANCE) / (MAX_TOLERANCE - MIN_TOLERANCE)
				spy_feedback = "Low"
			result["strokes-grade-data"][STROKE_STARTPOINT_LOCATION_Y].append(spy_score)
			result["strokes-feedback"][STROKE_STARTPOINT_LOCATION_Y].append(spy_feedback)
		else:
			spy_ratio_offset = sspy_ratio  -espy_ratio
			grade_stroke_by_ratio(spy_ratio_offset, DIFFERENCE_PARAMS,
				result, STROKE_STARTPOINT_LOCATION_Y, "High", "Low")

		# STROKES Endpoints (X,Y)
		eepx_ratio = (eepx - expected_x_min) / float(expected_width)
		eepy_ratio = (eepy - expected_y_min) / float(expected_height)
		sepx_ratio = (sepx - submitted_x_min) / float(submitted_width)
		sepy_ratio = (sepy - submitted_y_min) / float(submitted_height)
		if eepx_ratio == 0:
			# only allow halfway
			if sepx_ratio < MIN_TOLERANCE:
				epx_score = 1.0
				epx_feedback = "Acceptable"
			else:
				epx_score = 1 - (min(sepx_ratio, MAX_TOLERANCE) - MIN_TOLERANCE) / (MAX_TOLERANCE - MIN_TOLERANCE)
				epx_feedback = "Right"
			result["strokes-grade-data"][STROKE_ENDPOINT_LOCATION_X].append(epx_score)
			result["strokes-feedback"][STROKE_ENDPOINT_LOCATION_X].append(epx_feedback)
		else:
			epx_ratio_offset = sepx_ratio - eepx_ratio
			grade_stroke_by_ratio(epx_ratio_offset, DIFFERENCE_PARAMS,
				result, STROKE_ENDPOINT_LOCATION_X, "Left", "Right")
		if eepy_ratio == 0:
			# only allow halfway
			if sepy_ratio < MIN_TOLERANCE:
				epy_score = 1.0
				epy_feedback = "Acceptable"
			else:
				epy_score = 1 - (min(sepy_ratio, MAX_TOLERANCE) - MIN_TOLERANCE) / (MAX_TOLERANCE - MIN_TOLERANCE)
				epy_feedback = "Low"
			result["strokes-grade-data"][STROKE_ENDPOINT_LOCATION_Y].append(epy_score)
			result["strokes-feedback"][STROKE_ENDPOINT_LOCATION_Y].append(epy_feedback)
		else:
			epy_ratio_offset = sepy_ratio - eepy_ratio
			grade_stroke_by_ratio(epy_ratio_offset, DIFFERENCE_PARAMS,
				result, STROKE_ENDPOINT_LOCATION_Y, "High", "Low")

		# STROKES Shape - TODO
		n_expected_stroke_points = len(expected_stroke)
		n_submitted_stroke_points = len(submitted_stroke)
		steps = max(n_expected_stroke_points, n_submitted_stroke_points)
		if steps == n_expected_stroke_points:
			expected_step = 1
			submitted_step = float(n_submitted_stroke_points - 1) / float(n_expected_stroke_points - 1)
		else:
			expected_step = float(n_expected_stroke_points - 1) / float(n_submitted_stroke_points - 1)
			submitted_step = 1

		expected_cursor = 0
		submitted_cursor = 0
		
		wrong_count = 0
		wrong_count = 0
		# print es_width, es_height, ss_width, ss_height
		for j in range(steps):
			expected_step_index = int(expected_cursor)
			expected_step_mod = expected_cursor % 1.0
			submitted_step_index = int(submitted_cursor)
			submitted_step_mod = submitted_cursor % 1.0
			# [ex, ey] = grader.get_continuous_point(expected_stroke, expected_step_index, expected_step_mod)
			# [sx, sy] = grader.get_continuous_point(submitted_stroke, submitted_step_index, submitted_step_mod)
			[edx, edy] = grader.get_continuous_derivative(expected_stroke, expected_stroke_derivatives, expected_step_index, expected_step_mod)
			[sdx, sdy] = grader.get_continuous_derivative(submitted_stroke, submitted_stroke_derivatives, submitted_step_index, submitted_step_mod)
			# a = (ex - expected_x_min) / expected_width
			# b = (ey - expected_y_min) / expected_height
			# c = (sx - submitted_x_min) / submitted_width
			# d = (sy - submitted_y_min) / submitted_height
			# a = (ex - exmin) / es_width
			# b = (ey - eymin) / es_height
			# c = (sx - sxmin) / ss_width
			# d = (sy - symin) / ss_height
			# xval = c - a
			# yval = d - b
			# is_bad_point = (abs(xval) > 0.25) and (abs(yval) > 0.25) or abs(xval) > 0.5 or abs(yval) > 0.5
			e_angle = math.atan2(edx, edy)
			s_angle = math.atan2(sdx, sdy)
			angle_diff = (abs(e_angle - s_angle) % (2*math.pi) / (2*math.pi))
			is_bad_orientation = angle_diff > 0.2
			if is_bad_orientation:
				wrong_count += 1
			expected_cursor += expected_step
			submitted_cursor += submitted_step
		raw_stroke_shape_score = 1 - wrong_count / float(steps)
		stroke_shape_score = (min(raw_stroke_shape_score, STROKE_SHAPE_SCORE_TOLERANCE) - STROKE_SHAPE_SCORE_LIMIT) / (STROKE_SHAPE_SCORE_TOLERANCE - STROKE_SHAPE_SCORE_LIMIT)
		stroke_shape_score = max(stroke_shape_score,0)
		result["strokes-grade-data"][STROKE_SHAPE].append(stroke_shape_score)
		if stroke_shape_score == 1.0:
			# Acceptable
			shape_feedback = "Acceptable"
		else:
			# Irregular
			shape_feedback = "Irregular"
		result["strokes-feedback"][STROKE_SHAPE].append(shape_feedback)

	character_score = score(CHARACTER_GRADE_DATA, CHARACTER_GRADE_WEIGHTS)
	strokes_score = score(STROKE_GRADE_DATA, STROKE_GRADE_WEIGHTS)
	overall_score = character_score * GRADE_WEIGHTS["character"] + strokes_score * GRADE_WEIGHTS["strokes"]
	result["character-grade"] = character_score
	result["strokes-grade"] = strokes_score
	result["overall-grade"] = overall_score
	return result


@csrf_exempt
def student_submit(request):
	# Get character ID and submitted points from the request and evaluate
	try:
		if request.method == "POST":
			data = json.loads(request.body)
			character = Character.objects.get(unicode_value=data["character"]["unicode-value"])
			expected_points = json.loads(character.points)
			submitted_points = data["strokes"]
			results = evaluate(expected_points, submitted_points)
			response = {
				"results" : results
			}
			return HttpResponse(json.dumps(response), content_type="application/json")
		else:
			return HttpResponseNotAllowed(['POST'])
	except ObjectDoesNotExist:
		return HttpResponse(status=404)
	except Exception, e:
		# TODO: Error-Handling
		raise
