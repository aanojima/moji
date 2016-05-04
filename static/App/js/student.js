$(document).ready(function(){
	// TODO
	var exerciseManager = ExerciseManager();
	var feedbackManager = FeedbackManager();
	var studentSubmitter = StudentSubmitter(feedbackManager);
	var drawingPad = DrawingPad(studentSubmitter);
	window.drawingPad = drawingPad;
	window.studentSubmitter = studentSubmitter;
});