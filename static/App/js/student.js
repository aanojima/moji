$(document).ready(function(){
	// TODO
	var studentSubmitter = StudentSubmitter(); // TODO
	var drawingPad = DrawingPad(studentSubmitter);
	window.drawingPad = drawingPad;
	window.studentSubmitter = studentSubmitter;
});