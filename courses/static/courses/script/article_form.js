$(document).ready(function () {	
	var config = RichTextEditorConfig.Edit();
	// Set file upload URLs
	config.uploadUrl = '/courses/imageupload/';
	config.filebrowserBrowseUrl = '/courses/audiobrowse/';
	config.filebrowserImageBrowseUrl = '/courses/imagebrowse/';
	config.filebrowserUploadUrl = '/courses/audioupload/';
	config.filebrowserImageUploadUrl = '/courses/imageupload/';
	
	var editor = RichTextEditor.render(idRichTextEditor, config);
});