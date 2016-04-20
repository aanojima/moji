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
		for (var i in _strokes){
			console.log(self.calculateStrokeCOG(i));
		}
		console.log(self.calculateCOG());
		console.log(_strokes);
	}

	self.calculateCOG = function(){
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

	self.calculateStrokeCOG = function(strokeNumber){
		var numPoints = 0;
		var totalX = 0;
		var totalY = 0;
		var stroke = _strokes[strokeNumber];
		numPoints = stroke.length;
		for (var i in stroke){
			var point = stroke[i];
			totalX += point[0];
			totalY += point[1];
		}
		return [totalX / numPoints, totalY / numPoints];
	}

	self.calculateDeviation = function(){
		// TODO
	}

	self.calculateRange = function(){
		// TODO
	}

	self.calculateStrokeDeviation = function(strokeNumber){
		// TODO
	}

	self.calculateStrokeRange = function(strokeNumber){
		// TODO
	}

	self.calculateMultipleStrokeIntersections = function(){
		// TODO
	}

	self.caclulateSingleStrokeIntersections = function(){
		// TODO
	}

	self.submit = function(){
		// TODO
	}

	return self;
}