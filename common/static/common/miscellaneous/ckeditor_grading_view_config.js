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
	
	config.removePlugins = 'elementspath';
	config.allowedContent = true;
	config.readOnly = true;
	
	config.extraPlugins = 'comment';

	config.removeButtons = 'Subscript,Superscript,Styles,Blockquote';
	
	config.height = 500;
};