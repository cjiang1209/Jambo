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

	config.removePlugins= 'elementspath';
	config.removeButtons = 'Subscript,Superscript,Styles,Blockquote';
	
	config.extraPlugins = 'comment,placeholder,devtools';
};