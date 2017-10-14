var TemplateManager = function(drawingPad){
	var self = {};

	// TODO: Add File Upload
	$("#set-template-button").on("click", function(e){


		// // Via URL input
		// var URL = $("#template-url").val();
		// drawingPad.setBackgroundImage(URL);
		// $("#template-url").val("");
		// $("#template-modal").modal("hide");
	});

	$("#drawing-template").on("click", function(e){
		// Get Character from Box
		var s = $("#character-input").val() || '';
		var code = s.charCodeAt();
		if (isNaN(code)){
			return false;
		}
		var URL = "/api/character_images/" + String(code)
		drawingPad.setBackgroundImage(URL);
	});

	return self;
}
