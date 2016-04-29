CKEDITOR.editorConfig = function( config ) {
	config.toolbarGroups = [
	    { name: 'insert', groups: [ 'insert' ] }
	];
	
	config.removePlugins = 'elementspath';
	config.removeButtons = 'Image,Table,HorizontalRule,SpecialChar';
	config.allowedContent = true;
	config.readOnly = true;
	
	config.extraPlugins = 'comment';
};