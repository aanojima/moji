var FeedbackManager = function(){
	var self = {};

	function gradeFeedbackText(grade){
		return " (" + (100*grade.toFixed(2)) + "%)";
	}

	self.displayFeedback = function(results){
		console.log(results);
		// RESET
		$(".feedback").text("");
		$(".feedback-list").html("");

		// Overall Grade
		var overallGrade = results["overall-grade"];
		var overallGradeLetter = ""
		if (overallGrade < 0.60){
			overallGradeLetter = "F"
		}
		else if (overallGrade < 0.70){
			overallGradeLetter = "D"
		}
		else if (overallGrade < 0.80){
			overallGradeLetter = "C"
		}
		else if (overallGrade < 0.90){
			overallGradeLetter = "B"
		}
		else if (overallGrade < 1.00){
			overallGradeLetter = "A"
		}
		else {
			overallGradeLetter = "Perfect"
		}
		overallGradeLetter += gradeFeedbackText(overallGrade)
		$("#overall-grade").text(overallGradeLetter);

		// Character Grade
		var characterGrade = results["character-grade"];
		var characterGradeLetter = ""
		if (characterGrade < 0.60){
			characterGradeLetter = "F"
		}
		else if (characterGrade < 0.70){
			characterGradeLetter = "D"
		}
		else if (characterGrade < 0.80){
			characterGradeLetter = "C"
		}
		else if (characterGrade < 0.90){
			characterGradeLetter = "B"
		}
		else if (characterGrade < 1.00){
			characterGradeLetter = "A"
		}
		else {
			characterGradeLetter = "Perfect"
		}
		characterGradeLetter += gradeFeedbackText(characterGrade);
		$("#character-grade").text(characterGradeLetter);

		// Strokes Grade
		var strokesGrade = results["strokes-grade"];
		var strokesGradeLetter = ""
		if (strokesGrade < 0.60){
			strokesGradeLetter = "F"
		}
		else if (strokesGrade < 0.70){
			strokesGradeLetter = "D"
		}
		else if (strokesGrade < 0.80){
			strokesGradeLetter = "C"
		}
		else if (strokesGrade < 0.90){
			strokesGradeLetter = "B"
		}
		else if (strokesGrade < 1.00){
			strokesGradeLetter = "A"
		}
		else {
			strokesGradeLetter = "Perfect"
		}
		strokesGradeLetter += gradeFeedbackText(strokesGrade);
		$("#strokes-grade").text(strokesGradeLetter);

		// Stroke Count
		var strokeCount = results["character-feedback"]["character-stroke-count"]
		var strokeCountFeedback = "";
		var strokeCountGrade = results["character-grade-data"]["character-stroke-count"];
		if (strokeCount == 0){
			// PERFECT
			strokeCountFeedback = "Perfect";
		}
		else if (strokeCount < 0){
			// MISSING STROKES
			strokeCountFeedback = "Missing " + Math.abs(strokeCount) + " strokes";
		}
		else {
			// TOO MANY STROKES
			strokeCountFeedback = Math.abs(strokeCount) + " too many strokes";
		}
		strokeCountFeedback += gradeFeedbackText(strokeCountGrade);
		$("#stroke-count").text(strokeCountFeedback);
		if (strokeCount != 0){
			$("#stroke-count").text(strokeCountFeedback);
			$("#feedback-modal").modal("show");
			return;
		}

		// Dimensional Ratio
		var dimensionalRatioFeedback = results["character-feedback"]["character-dimension-ratio"]
		var dimensionalRatioGrade = results["character-grade-data"]["character-dimension-ratio"]
		$("#dimensional-ratio").text(dimensionalRatioFeedback + gradeFeedbackText(dimensionalRatioGrade));

		// Cross-Intersections
		var crossIntersections = results["character-feedback"]["character-cross-intersections"];
		var crossIntersectionsFeedback = "";
		if (crossIntersections == 0){
			// PERFECT
			crossIntersectionsFeedback = "Perfect";
		}
		else if (crossIntersections < 0){
			// Missing Cross-Intersections
			crossIntersectionsFeedback = "Missing " + Math.abs(crossIntersections) + " multi-stroke intersections";
		}
		else {
			// Too Many Cross-Intersections
			crossIntersectionsFeedback = Math.abs(crossIntersections) + " too many multi-stroke intersections"
		}
		var crossIntersectionsGrade = results["character-grade-data"]["character-cross-intersections"];
		$("#cross-intersections").text(crossIntersectionsFeedback + gradeFeedbackText(crossIntersectionsGrade));

		// TODO: Cross-Intersections Locations - LATER

		// Stroke Width
		for (var i in results["strokes-feedback"]["stroke-width"]){
			var strokeWidthGrade = results["strokes-grade-data"]["stroke-width"][i];
			var strokeWidthFeedback = results["strokes-feedback"]["stroke-width"][i] + gradeFeedbackText(strokeWidthGrade);
			var strokeWidthFeedbackEl = $("<li></li>").text(strokeWidthFeedback).css("font-weight", "Bold");
			$("#strokes-width-list").append(strokeWidthFeedbackEl);
		}
		
		// Stroke Height
		for (var i in results["strokes-feedback"]["stroke-height"]){
			var strokeHeightGrade = results["strokes-grade-data"]["stroke-height"][i];
			var strokeHeightFeedback = results["strokes-feedback"]["stroke-height"][i] + gradeFeedbackText(strokeHeightGrade);
			var strokeHeightFeedbackEl = $("<li></li>").text(strokeHeightFeedback).css("font-weight", "Bold");
			$("#strokes-height-list").append(strokeHeightFeedbackEl);
		}

		// Self-Intersections
		var selfIntersections = results["strokes-feedback"]["stroke-self-intersections"];
		var selfIntersectionsFeedback = "";
		if (selfIntersections == 0){
			// PERFECT
			selfIntersectionsFeedback = "Perfect";
		}
		else if (selfIntersections < 0){
			// Missing Self-Intersections
			selfIntersectionsFeedback = "Missing " + Math.abs(selfIntersections) + " self-stroke intersections";
		}
		else {
			// Too Many Self-Intersections
			selfIntersectionsFeedback = Math.abs(selfIntersections) + " too many self-stroke intersections"
		}
		var selfIntersectionsGrade = results["strokes-grade-data"]["stroke-self-intersections"];
		$("#self-intersections").text(selfIntersectionsFeedback + gradeFeedbackText(selfIntersectionsGrade));


		// Stroke Location
		for (var i in results["strokes-feedback"]["stroke-range-location-x"]){
			var strokeHorizontalFeedback = results["strokes-feedback"]["stroke-range-location-x"][i];
			var strokeVerticalFeedback = results["strokes-feedback"]["stroke-range-location-y"][i];
			if (strokeHorizontalFeedback != "Acceptable"){
				strokeHorizontalFeedback = "Too " + strokeHorizontalFeedback;
			}
			if (strokeVerticalFeedback != "Acceptable"){
				strokeVerticalFeedback = "Too " + strokeVerticalFeedback;
			}
			var strokeHorizontalGrade = results["strokes-grade-data"]["stroke-range-location-x"][i]
			var strokeVerticalGrade = results["strokes-grade-data"]["stroke-range-location-y"][i]
			var strokePositionFeedbackEl = $("<li></li>")
				.text("Horizontal - " + strokeHorizontalFeedback + gradeFeedbackText(strokeHorizontalGrade) + 
					",  Vertical - " + strokeVerticalFeedback + gradeFeedbackText(strokeVerticalGrade))
				.css("font-weight", "Bold");
			$("#strokes-position-list").append(strokePositionFeedbackEl);
		}

		// TODO: LATER
		// STROKE_STARTPOINT_LOCATION_X = "stroke-startpoint-location-x"
		// STROKE_STARTPOINT_LOCATION_Y = "stroke-startpoint-location-y"
		// STROKE_ENDPOINT_LOCATION_X = "stroke-endpoint-location-x"
		// STROKE_ENDPOINT_LOCATION_Y = "stroke-endpoint-location-y"

		// STROKE_SHAPE = "stroke-shape"
		for (var i in results["strokes-feedback"]["stroke-shape"]){
			var strokeShapeFeedback = results["strokes-feedback"]["stroke-shape"][i];
			var strokeShapeGrade = results["strokes-grade-data"]["stroke-shape"][i];
			var strokeShapeFeedbackEl = $("<li></li>")
				.text(strokeShapeFeedback + gradeFeedbackText(strokeShapeGrade))
				.css("font-weight", "Bold");
			$("#strokes-shape-list").append(strokeShapeFeedbackEl);
		}

		$("#feedback-modal").modal("show");
	}

	return self;
}