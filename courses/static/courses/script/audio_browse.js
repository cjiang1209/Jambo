$(document).ready(function () {	
	$(document).on('click', '.audio-link', function () {
		window.opener.CKEDITOR.tools.callFunction(CKEditorFuncNum, $(this).data('url'));
		window.close();
	});
});