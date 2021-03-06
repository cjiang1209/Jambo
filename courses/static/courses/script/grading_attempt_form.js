$(document).ready(function () {
	$('#form_update_grade').on('submit', function (evt) {
		evt.preventDefault();
		
		var form = $(this);
		var grade = form.find('input[name="' + nameGrade + '"]').val();
		
		$.post(urlUpdateGrade, {
			grade: grade
		}).done(function (data) {
			$.alert({
			    title: 'Updated',
			    content: 'Grade updated successfully.',
			    backgroundDismiss: true
			});
		});
	});
	
	var config = RichTextEditorConfig.Comment();
	var rteditor = RichTextEditor.render(idRichTextEditor, config);
	rteditor.supportComment(commentUrlConfig, false);
});