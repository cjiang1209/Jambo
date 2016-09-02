$(document).ready(function () {	
	var config = RichTextEditorConfig.Edit();
	// Set file upload URLs
	config.uploadUrl = '/courses/imageupload/';
	config.filebrowserBrowseUrl = '/ckfinder/ckfinder.html';
	config.filebrowserImageBrowseUrl = '/courses/imagebrowse/';
	config.filebrowserUploadUrl = '/ckfinder/core/connector/php/connector.php?command=QuickUpload&type=Files';
	config.filebrowserImageUploadUrl = '/courses/imageupload/';
	
	var editor = RichTextEditor.render(idRichTextEditor, config);
});