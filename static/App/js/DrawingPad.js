var DrawingPad = function(submitter){
	var self = {};

	var _isDrawing = false;
	var _canvas = $("#drawing-canvas")[0];
	var _context = _canvas.getContext("2d");
	var _character = Character();
	window.character = _character;
	var _lastStrokeData = [];

	var debugToggle = false;

	// TODO
	$("#drawing-canvas").on("mousedown", function(e){
		var x = e.offsetX / 2;
		var y = e.offsetY / 2;
		beginStroke(x,y);
		beginDraw(x,y);
	});

	$("#drawing-canvas").on("mousemove", function(e){
		if (_isDrawing){
			var x = e.offsetX / 2;
			var y = e.offsetY / 2;
			stroke(x,y);
			draw(x,y);
		}
	});

	$(document).on("mouseup", function(e){
		if (_isDrawing){
			// STROKE COMPLETED
			var x = e.offsetX / 2;
			var y = e.offsetY / 2;
			endStroke(x,y);
			endDraw(x,y);
		}
		_isDrawing = false;
	});

	$("#drawing-submit").on("click", function(e){
		submit();
	});

	$("#drawing-undo").on("click", function(e){
		undoStroke();
		resetDraw();
	});

	$("#drawing-clear").on("click", function(e){
		_character.clear();
		clear();
	});

	$("#drawing-debug").on("click", function(e){
		debugToggle = !debugToggle;
		if (debugToggle){
			self.debug();
			$(this).text("Reset");
		}
		else {
			resetDraw();
			$(this).text("Debug");
		}
	});

	function beginDraw(x,y){
		_context.beginPath();
		_context.moveTo(x,y);
	}

	function beginStroke(x,y){
		_lastStrokeData.push([x,y]);
		_isDrawing = true;
	}

	function draw(x,y){
		_context.lineTo(x,y);
		_context.strokeStyle = "black";
		_context.lineWidth = 2;
		_context.stroke();
	}

	function stroke(x,y){
		var lastIndex = _lastStrokeData.length - 1;
		if (lastIndex > 0){
			var lastPoint = _lastStrokeData[lastIndex];
			if (lastPoint[0] == x && lastPoint[1] == y){
				// Same point - ignore
				return;
			}
		}
		if (lastIndex > 1){
			var lastPoint = _lastStrokeData[lastIndex];
			var prevLastPoint = _lastStrokeData[lastIndex - 1];
			var dy = y - lastPoint[1];
			var dx = x - lastPoint[0];
			var prevDY = lastPoint[1] - prevLastPoint[1];
			var prevDX = lastPoint[0] - prevLastPoint[0];
			if (dx == 0 && prevDX == 0){
				// Same vertical slope - replace old point
				_lastStrokeData.pop();
			}
			else if ((dy/dx) == (prevDY/prevDX)){
				// Same slope - replace old point
				_lastStrokeData.pop();
			}
		}
		_lastStrokeData.push([x,y]);
	}

	function endDraw(x,y){
		// draw(x,y);
	}

	function endStroke(x,y){
		// TODO
		_character.addNewStroke(_lastStrokeData);
		_lastStrokeData = [];
	}

	function submit(){
		submitter.process(_character);
		submitter.submit();
	}

	function undoStroke(){
		var lastStroke = _character.removeLastStroke();
	}

	function resetDraw(){
		clear();
		var strokes = _character.getStrokes();
		for (var i in strokes){
			var stroke = strokes[i];
			for (var j in stroke){
				var point = stroke[j];
				var x = point[0];
				var y = point[1];
				if (j == 0){
					beginDraw(x,y);
				}
				else if (j == strokes.length - 1){
					endDraw(x,y);
				}
				else {
					draw(x,y);
				}
			}
		}
	}

	function clear(){
		_context.clearRect(0,0,275,275);
	}

	function next(){
		// TODO
	}

	self.showCOG = function(){
		// TODO
		var COG = _character.calculateCOG();
		var x = COG[0];
		var y = COG[1];
		_context.fillStyle = "red";
		_context.fillRect(x-1,y-1,3,3);
	}

	self.showStrokeCOGs = function(){
		// TODO
		var COGs = _character.calculateStrokeCOGs();
		for (var i in COGs){
			var COG = COGs[i];
			var x = COG[0];
			var y = COG[1];
			_context.fillStyle = "red";
			_context.fillRect(x-1,y-1,3,3);
		}
	}

	self.debug = function(){
		_character.debug();
		
		var derivatives = _character.calculateDerivatives();
		var points = _character.getStrokes();
		for (var i in derivatives){
			var strokeDerivatives = derivatives[i];
			var strokePoints = points[i];
			drawGradients(strokePoints, strokeDerivatives);
		}

		var endpoints = _character.getEndpoints();
		for (var i in endpoints){
			var strokeEndpoints = endpoints[i];
			encirclePoints(strokeEndpoints, "red");
		}
		
		var lineSegments = _character.sortLineSegments();
		// console.log(lineSegments);

		var intersections = _character.calculateIntersections();
		// console.log(intersections);

		var singleStrokeIntersections = [];
		for (var i in intersections["single"]){
			var intersection = intersections["single"][i];
			singleStrokeIntersections.push(intersection["point"]);
		}
		encirclePoints(singleStrokeIntersections, "green");

		var multipleStrokeIntersections = [];
		for (var i in intersections["multiple"]){
			var intersection = intersections["multiple"][i];
			multipleStrokeIntersections.push(intersection["point"])
		}
		encirclePoints(multipleStrokeIntersections, "orange");

		self.showCOG();
		self.showStrokeCOGs();

		var range = _character.calculateRange();
		boxRectangle(range, "brown");
		var strokeRanges = _character.calculateStrokeRanges();
		// console.log(range, strokeRanges);
		for (var i in strokeRanges){
			boxRectangle(strokeRanges[i], "brown");
		}

	}

	function boxRectangle(range, color){
		_context.strokeStyle = color;
		_context.strokeRect(range[0], range[1], range[2]-range[0], range[3]-range[1]);

	}

	function encirclePoints(points, color){
		var CIRCLE_RADIUS = 5;
		for (var i in points){
			var point = points[i];
			var x = point[0];
			var y = point[1];
			_context.strokeStyle = color;
			_context.beginPath();
			_context.arc(x,y,CIRCLE_RADIUS,0,2*Math.PI);
			_context.stroke();
		}
	}

	function drawGradients(points, derivatives){
		var GRADIENT_MAGNITUDE = 10; // configurable
		for (var i in derivatives){
			var derivative = derivatives[i];
			var dx = derivative[0];
			var dy = derivative[1];
			// normalize
			var magnitude = Math.sqrt(dx*dx + dy*dy);
			var ndx = dx / magnitude;
			var ndy = dy / magnitude;
			var gx = -1*ndy;
			var gy = ndx;
			// draw gradient from point
			var point = points[i];
			var x = point[0];
			var y = point[1];
			// draw
			_context.beginPath();
			_context.moveTo(x,y);
			_context.lineTo(x+GRADIENT_MAGNITUDE*gx,y+GRADIENT_MAGNITUDE*gy);
			_context.strokeStyle = "blue";
			_context.lineWidth = 2;
			_context.stroke();
		}
	}

	self.setPoints = function(points){
		_character.setPoints(points)
		resetDraw();
	}

	self.setBackgroundImage = function(imageURL){
		var feedbackCanvas = $("#feedback-canvas")[0];
		var context = feedbackCanvas.getContext("2d");
		var imageObj = new Image();
		imageObj.onload = function(){
			context.drawImage(this, 0, 0, feedbackCanvas.width, feedbackCanvas.height);
		};

		imageObj.src = imageURL;
	}

	return self;
}
