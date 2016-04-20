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
		console.log(_strokes);
	}

	return self;
}