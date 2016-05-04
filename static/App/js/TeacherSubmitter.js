var TeacherSubmitter = function(){
	var self = {};
	var data = {
		"character" : {},
		"strokes" : []
	};

	var processCharacter = function(){
		var unicodeValue = $("#character-input").val().charCodeAt(0);
		data["character"] = {
			"unicode-value" : unicodeValue
		};
	}

	var processStrokes = function(character){
		data["strokes"] = character.getStrokes()
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
			method : "PUT",
			url : window.MOJI_URL + "api/characters/" + data["character"]["unicode-value"],
			data : JSON.stringify(data),
			success : function(result){
				console.log(result);
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
