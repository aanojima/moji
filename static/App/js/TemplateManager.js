var TemplateManager = function(drawingPad){
	var self = {};

	// TODO
	$("#set-template-button").on("click", function(e){
		var URL = $("#template-url").val();
		drawingPad.setBackgroundImage(URL);
		$("#template-url").val("");
		$("#template-modal").modal("hide");
	});

	return self;
}