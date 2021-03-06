var Character = function(){
	var self = {};

	var _strokes = [];

	self.addNewStroke = function(data){
		var points = [];
		for (var i in data){
			var point = [data[i][0], data[i][1]];
			points.push(point);
		}
		_strokes.push(points);
	}

	self.clear = function(){
		_strokes = [];
	}

	self.removeLastStroke = function(){
		return _strokes.pop();
	}

	self.getStrokes = function(){
		var _strokesCopy = [];
		for (var i in _strokes){
			// Stroke
			_strokesCopy.push([]);
			for (var j in _strokes[i]){
				// Point
				_strokesCopy[i].push([]);
				var x = _strokes[i][j][0];
				var y = _strokes[i][j][1];
				_strokesCopy[i][j].push(x,y);
			}
		}
		return _strokesCopy;
	}

	self.getStrokeCount = function(){
		return _strokes.length;
	}

	self.debug = function(){
		//console.log(self.calculateStrokeCOGs());
		//console.log(self.calculateCOG());
		//console.log(_strokes);
	}

	self.getEndpoints = function(){
		var endpoints = [];
		for (var i in _strokes){
			// TODO
			var stroke = _strokes[i];
			var start = stroke[0];
			var end = stroke[stroke.length - 1];
			var strokeEndpoints = [
				[start[0], start[1]],
				[end[0], end[1]]
			];
			endpoints.push(strokeEndpoints);
		}
		return endpoints;
	}

	self.calculateCOG = function(){
		// TODO: should this be based off pixels or stroke data?
		// PIXELS
		var numPoints = 0;
		var totalX = 0;
		var totalY = 0;
		for (var i in _strokes){
			var stroke = _strokes[i];
			numPoints += stroke.length;
			for (var j in stroke){
				var point = stroke[j];
				totalX += point[0];
				totalY += point[1];
			}
		}
		return [totalX / numPoints, totalY / numPoints];
	}

	self.calculateStrokeCOGs = function(){
		// TODO: should this be based off pixels or stroke data?
		// IDK: how do we get pixels for stroke though?
		var strokeCOGs = [];
		for (var i in _strokes){
			var stroke = _strokes[i];
			var numPoints = 0;
			var totalX = 0;
			var totalY = 0;
			numPoints = stroke.length;
			for (var j in stroke){
				var point = stroke[j];
				totalX += point[0];
				totalY += point[1];
			}
			var COG = [totalX / numPoints, totalY / numPoints];
			strokeCOGs.push(COG);
		}
		return strokeCOGs;	
	}

	self.calculateDerivatives = function(){
		var derivatives = [];
		for (var i in _strokes){
			var strokeDerivatives = [];
			var stroke = _strokes[i];
			for (var j in stroke){
				j = parseInt(j);
				var point = stroke[j];
				var dx = 0;
				var dy = 0;
				if (j == 0){
					// FIRST
					var nextPoint = stroke[j+1];
					dx = nextPoint[0] - point[0];
					dy = nextPoint[1] - point[1];
				}
				else if (j == stroke.length - 1){
					// LAST
					var prevPoint = stroke[j-1];
					dx = point[0] - prevPoint[0];
					dy = point[1] - prevPoint[1];
				}
				else {
					// INBETWEEN
					var prevPoint = stroke[j-1];
					var nextPoint = stroke[j+1];
					dx = 0.5*(nextPoint[0] - prevPoint[0]);
					dy = 0.5*(nextPoint[1] - prevPoint[1]);
				}
				if (dx == 0){
					// small margin of error
					dx = 0.001;
				}
				if (dy == 0){
					dy = 0.001;
				}
				var pointDerivative = [dx, dy];
				strokeDerivatives.push(pointDerivative);
			}
			derivatives.push(strokeDerivatives);
		}
		return derivatives;
	}

	self.getLineSegments = function(){
		// Create line segments
		var lineSegments = [];
		for (var i in _strokes){
			var stroke = _strokes[i];
			for (var j in stroke){
				var point = stroke[j];
				if (j < stroke.length - 1){
					// Not the last point
					var nextPoint = stroke[parseInt(j) + 1];
					var left = undefined;
					var right = undefined;
					if (point[0] <= nextPoint[0]){
						left = point;
						right = nextPoint;
					}
					else
					{
						left = nextPoint;
						right = point;
					}
					var lineSegment = {
						"stroke" : i,
						"segment" : j,
						"left" : left,
						"right" : right
					};
					lineSegments.push(lineSegment);
				}
			}
		}

		return lineSegments;
	}

	self.sortLineSegments = function(){
		var lineSegments = self.getLineSegments();
		
		// Sort line segments
		lineSegments.sort(function(a,b){
			return Math.sign(a["left"][0] - b["left"][0]);
		});
		
		return lineSegments
	}

	self.calculateRange = function(){
		var strokeRanges = self.calculateStrokeRanges();
		var Xmin = Infinity;
		var Ymin = Infinity;
		var Xmax = -Infinity;
		var Ymax = -Infinity;
		for (var i in strokeRanges){
			var range = strokeRanges[i];
			Xmin = Math.min(Xmin, range[0]);
			Ymin = Math.min(Ymin, range[1]);
			Xmax = Math.max(Xmax, range[2]);
			Ymax = Math.max(Ymax, range[3]);
		}
		return [Xmin, Ymin, Xmax, Ymax];
	}

	self.calculateStrokeRanges = function(){
		var strokeRanges = [];
		for (var i in _strokes){
			var stroke = _strokes[i];
			var strokeXmin = Infinity;
			var strokeYmin = Infinity;
			var strokeXmax = -Infinity;
			var strokeYmax = -Infinity;
			for (var j in stroke){
				var point = stroke[j];
				strokeXmin = Math.min(strokeXmin, point[0]);
				strokeYmin = Math.min(strokeYmin, point[1]);
				strokeXmax = Math.max(strokeXmax, point[0]);
				strokeYmax = Math.max(strokeYmax, point[1]);
			}
			var strokeRange = [strokeXmin, strokeYmin, strokeXmax, strokeYmax];
			strokeRanges.push(strokeRange);
		}
		return strokeRanges;
	}

	// TODO: Update backend for all intersection methods
	function calculateLineSegmentIntersection(lineA, lineB){
		var p0_x = lineA["left"][0];
		var p1_x = lineA["right"][0];
		var p0_y = lineA["left"][1];
		var p1_y = lineA["right"][1];
		var p2_x = lineB["left"][0];
		var p3_x = lineB["right"][0];
		var p2_y = lineB["left"][1];
		var p3_y = lineB["right"][1];

		var s1_x = p1_x - p0_x;
		var s1_y = p1_y - p0_y;
		var s2_x = p3_x - p2_x;
		var s2_y = p3_y - p2_y;

		var s = (-1*s1_y * (p0_x - p2_x) + s1_x * (p0_y - p2_y)) / (-1*s2_x * s1_y + s1_x * s2_y);
		var t = (   s2_x * (p0_y - p2_y) - s2_y * (p0_x - p2_x)) / (-1*s2_x * s1_y + s1_x * s2_y);

		if (lineA["stroke"] == lineB["stroke"]){
			var segA = parseInt(lineA["segment"]);
			var segB = parseInt(lineB["segment"]);
			if (s >= 0 && s <= 1 && t >= 0 && t <= 1 &&
				Math.abs(segA - segB) > 1){
				// Stroke Self-Collision detected
				var ix = p0_x + (t * s1_x);
				var iy = p0_y + (t * s1_y);
				var intersection = {
					"point" : [ix, iy],
					"segmentA" : lineA,
					"segmentB" : lineB
				}
				return intersection;
			}
		}
		else {
			if (s >= 0 && s <= 1 && t >= 0 && t <= 1){
				// Stroke Inter-Collision detected
				var ix = p0_x + (t * s1_x);
				var iy = p0_y + (t * s1_y);
				var intersection = {
					"point" : [ix, iy],
					"segmentA" : lineA,
					"segmentB" : lineB
				};
				return intersection;
			}	
		}
		return undefined
	}

	self.calculateIntersections = function(){
		// TODO: Using AVL Tree and Line Sweep Method
		var intersections = {
			"multiple" : [],
			"single" : []
		};
		var lineSegments = self.getLineSegments();
		for (var i = 0; i < lineSegments.length; i++){
			var lineA = lineSegments[i];
			for (var j = i + 1; j < lineSegments.length; j++){
				var lineB = lineSegments[j];
				var intersection = calculateLineSegmentIntersection(lineA, lineB);
				if (intersection !== undefined){
					if (lineA["stroke"] == lineB["stroke"]){
						var lastIndex = intersections["single"].length - 1;
						if (lastIndex == -1){
							intersections["single"].push(intersection);
							continue;
						}
						var lastIntersection = intersections["single"][lastIndex];
						var p0 = lastIntersection["point"];
						var p1 = intersection["point"];
						var d = Math.sqrt(Math.pow(p1[0]-p0[0],2)+Math.pow(p1[1]-p0[1],2));
						if (d > 5){
							intersections["single"].push(intersection);
						}
					}
					else {
						var lastIndex = intersections["multiple"].length - 1;
						if (lastIndex == -1){
							intersections["multiple"].push(intersection);
							continue;
						}
						var lastIntersection = intersections["multiple"][lastIndex];
						var p0 = lastIntersection["point"];
						var p1 = intersection["point"];
						var d = Math.sqrt(Math.pow(p1[0]-p0[0],2)+Math.pow(p1[1]-p0[1],2));
						if (d > 5){
							intersections["multiple"].push(intersection);
						}
					}
				}
			}
		}
		// console.log(intersections);
		return intersections;
	}

	self.setPoints = function(points){
		_strokes = points;
	}

	return self;
}
