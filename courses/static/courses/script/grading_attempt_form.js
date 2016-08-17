$(document).ready(function () {
	$('#form_update_grade').on('submit', function (evt) {
		evt.preventDefault();
		
		var form = $(this);
		var grade = form.find('input[name="' + nameGrade + '"]').val();
		
		$.post(urlUpdateGrade, {
			grade: grade
		}, function (data) {
			alert("Grade updated successfully");
		});
	});
	
	var rteditor = RichTextEditor.render('id_content', editorConfig);
	rteditor.supportComment(commentUrlConfig, false);
});