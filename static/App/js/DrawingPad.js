var DrawingPad = function(){
	var self = {};

	var _isDrawing = false;
	var _canvas = $("#drawing-canvas");
	var _context = _canvas[0].getContext("2d");
	var _character = Character();
	var _lastStrokeData = [];

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

	$("#drawing-undo").on("click", function(e){
		undoStroke();
		undoDraw();
	});

	$("#drawing-clear").on("click", function(e){
		_character.clear();
		clear();
	});

	function beginDraw(x,y){
		_context.beginPath();
		_context.moveTo(x,y);
	}

	function beginStroke(x,y){
		_isDrawing = true;
		_lastStrokeData.push([x,y]);
	}

	function draw(x,y){
		_context.lineTo(x,y);
		_context.strokeStyle = "#000";
		_context.lineWidth = 2;
		_context.stroke();
	}

	function stroke(x,y){
		_lastStrokeData.push([x,y]);
	}

	function endDraw(x,y){
		draw(x,y);
	}

	function endStroke(x,y){
		// TODO
		_lastStrokeData.push([x,y]);
		_character.addNewStroke(_lastStrokeData);
		_lastStrokeData = [];
	}

	function submit(){
		// TODO
	}

	function undoStroke(){
		var lastStroke = _character.removeLastStroke();
	}

	function undoDraw(){
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

	self.debug = function(){
		_character.debug();
	}

	return self;
}