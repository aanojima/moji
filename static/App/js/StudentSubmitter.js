var StudentSubmitter = function(feedbackManager){
	var self = {};
	var data = {
		"character" : {},
		"strokes" : [],
		// "intersections" : {},
		// "derivatives" : []
	};

	var processCharacter = function(){
		var characterSet = $("#character-set-select").val();
		var characterID = $("#character-select").val();
		var characterName = $("#character-select option:selected").attr("name");
		data["character"] = {
			"character-set" : characterSet,
			"character-id" : characterID,
			"character-name" : characterName
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
		// TODO
		// processImage(canvas);
		processCharacter()
		processStrokes(character);
		// processIntersections(character);
		// processDerivatives(character);
		// console.log(data);
	}

	self.submit = function(){
		// TODO: AJAX
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
