CKEDITOR.editorConfig = function( config ) {
	config.toolbarGroups = [
	    { name: 'basicstyles', groups: [ 'basicstyles', 'cleanup' ] },
		{ name: 'clipboard', groups: [ 'clipboard', 'undo' ] },
		{ name: 'paragraph', groups: [ 'list', 'indent', 'blocks', 'align', 'bidi', 'paragraph' ] },
		{ name: 'styles', groups: [ 'styles' ] },
		{ name: 'editing', groups: [ 'spellchecker'] },
		{ name: 'insert', groups: [ 'insert' ] },
		{ name: 'tools', groups: [ 'tools' ] },
		{ name: 'document', groups: [ 'mode', 'document', 'doctools' ] }
	];

	//config.extraPlugins = 'notification,notificationaggregator,filetools,uploadwidget,uploadimage';
	config.extraPlugins = 'uploadimage,image2';
	config.removePlugins= 'elementspath';
	config.removeButtons = 'Subscript,Superscript,Styles,Blockquote';
	config.allowedContent = true;
	
	config.height = 500;
	
	config.uploadUrl = '/courses/imageupload/';
	config.filebrowserBrowseUrl = '/ckfinder/ckfinder.html';
	config.filebrowserImageBrowseUrl = '/ckfinder/ckfinder.html?type=Images';
	config.filebrowserUploadUrl = '/ckfinder/core/connector/php/connector.php?command=QuickUpload&type=Files';
	config.filebrowserImageUploadUrl = '/courses/imageupload/';
};