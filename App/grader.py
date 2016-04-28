def get_stroke_count(points):
	return len(points)

def get_endpoints(points):
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

def calculate_COG(points):
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

def calculate_stroke_COGs(points):
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

def calculate_derivatives(points):
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

def get_line_segments(points):
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

def calculate_stroke_ranges(points):
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

def calculate_range(points):
	stroke_ranges = calculate_stroke_ranges(points)
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

def calculate_line_segment_intersections(lineA, lineB):
	p0_x = lineA["left"][0]
	p1_x = lineA["right"][0]
	p0_y = lineA["left"][1]
	p1_y = lineA["right"][1]
	p2_x = lineB["left"][0]
	p3_x = lineB["right"][0]
	p2_y = lineB["left"][1]
	p3_y = lineB["right"][1]

	s1_x = p1_x - p0_x
	s1_y = p1_y - p0_y
	s2_x = p3_x - p2_x
	s2_y = p3_y - p2_y

	d = -1*s2_x * s1_y + s1_x * s2_y
	if d == 0:
		return None

	s = float(-1*s1_y * (p0_x - p2_x) + s1_x * (p0_y - p2_y)) / d
	t = float(   s2_x * (p0_y - p2_y) - s2_y * (p0_x - p2_x)) / d

	if lineA["stroke"] == lineB["stroke"]:
		segA = lineA["segment"]
		segB = lineB["segment"]
		if s >= 0 and s <= 1 and t >= 0 and t <= 1 and abs(segA - segB) > 1:
			# Stroke Self-Collision detected
			ix = p0_x + (t * s1_x)
			iy = p0_y + (t * s1_y)
			intersection = {
				"point" : [ix, iy],
				"segmentA" : lineA,
				"segmentB" : lineB
			}
			return intersection
	else:
		if s >= 0 and s <= 1 and t >= 0 and t <= 1:
			# Stroke Inter-Collision detected
			ix = p0_x + (t * s1_x)
			iy = p0_y + (t * s1_y)
			intersection = {
				"point" : [ix, iy],
				"segmentA" : lineA,
				"segmentB" : lineB
			}
			return intersection

	return None

def calculate_intersections(points):
	# TODO: Using AVL Tree and Line Sweep Method
	intersections = {
		"multiple" : [],
		"single" : []
	}
	line_segments = get_line_segments(points)
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