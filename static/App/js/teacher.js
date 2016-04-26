$(document).ready(function(){
	// TODO
	var teacherSubmitter = TeacherSubmitter();
	var drawingPad = DrawingPad(teacherSubmitter);
	window.drawingPad = drawingPad;
	window.teacherSubmitter = teacherSubmitter;
});