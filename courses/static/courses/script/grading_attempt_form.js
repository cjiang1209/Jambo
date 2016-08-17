$(document).ready(function () {
	$('#form_update_grade').on('submit', function (evt) {
		evt.preventDefault();
		
		var form = $(this);
		var grade = form.find('input[name="' + nameGrade + '"]').val();
		
		console.log(grade);
		
		$.post(urlUpdateGrade, {
			grade: grade
		}, function (data) {
			console.log(grade);
		});
	});
	
	var rteditor = RichTextEditor.render('id_content', editorConfig);
	rteditor.supportComment(commentUrlConfig, false);
});