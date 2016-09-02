$(document).ready(function () {	
	$(document).on('click', '.js-image-link', function () {
		window.opener.CKEDITOR.tools.callFunction(CKEditorFuncNum, $(this).data('url'));
		window.close();
	});
});