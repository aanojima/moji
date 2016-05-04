var StudentSubmitter = function(feedbackManager){
	var self = {};
	var data = {
		"character" : {},
		"strokes" : []
	};

	var processCharacter = function(){
		var unicodeValue = parseInt($("#character-select").val());
		data["character"] = {
			"unicode-value" : unicodeValue
		};
	}

	var processStrokes = function(character){
		data.strokes = character.getStrokes()
	}

	var processIntersections = function(character){
		data.intersections = JSON.stringify(character.calculateIntersections());
	}

	var processDerivatives = function(character){
		data.derivatives = JSON.stringify(character.calculateDerivatives());
	}

	self.process = function(character){
		processCharacter()
		processStrokes(character);
	}

	self.submit = function(){
		$.ajax({
			method : "POST",
			url : window.MOJI_URL + "api/exercise/submit",
			data : JSON.stringify(data),
			success : function(result){
				feedbackManager.displayFeedback(result.results);
			},
			error : function(error){
				console.log(error.responseText);
			}
		})
	}

	self.debug = function(){
		self.process();
		// console.log(data);
	}

	return self;
}
