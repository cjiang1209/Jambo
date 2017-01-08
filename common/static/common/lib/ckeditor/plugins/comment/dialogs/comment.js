CKEDITOR.dialog.add('commentDialog', function(editor) {
	return {
		title: 'Comment',
		minWidth: 600,
		minHeight: 400,
		contents: [
			{
				id: 'cke_info',
				label: 'Comment',
				title: 'Comment',
				elements: [
					// Dialog window UI elements.
					{
						id: 'cke_comment_id',
						type: 'html',
						html: '',
						setup: function(widget) {
							this.setValue(-1);
						},
						commit: function(widget) {
							console.log('commit id');
							widget.setData('comment_id', this.getValue());
						}
					},
					{
						type: 'button',
						label: 'Insert a Pre-defined Comment',
						onClick: function() {
							var id = this.getDialog().getContentElement('cke_info', 'cke_content').getInputElement().getId();
							var ref = CKEDITOR.tools.addFunction(function (data) {
								CKEDITOR.instances[id].insertHtml(data);
							});
							window.open('/courses/predefinedcomment/browse/?CKEditor=' + id + '&CKEditorFuncNum=' + ref,
								'Insert a Pre-defined Comment',
								'width=1200, height=900');
						}
					},
					{
						id: 'cke_content',
						type: 'textarea',
						style: 'width: 100%;',
						label: 'Your comment',
						'default': '',
						required: true,
						onLoad: function(widget) {
							var editorConfig = RichTextEditorConfig.EditComment();
							var editor = CKEDITOR.replace(this.getInputElement().getId(), editorConfig);
							editor.on('change', function() {
								editor.updateElement();
							});
						},
						setup: function(widget) {
							//this.setValue(this['default']);
							CKEDITOR.instances[this.getInputElement().getId()].setData(this['default']);
						},
					},
				]
			},
		],
		buttons: [
		    {
		    	type: 'button',
		    	id: 'cke_btn_ajax_ok',
		        label: 'OK',
		        title: 'OK',
		        onClick: function(evt) {
		        	var dialog = evt.data.dialog;
		        	console.log('fire commit comment');
		        	dialog.fire('commitComment', {
		        		success: function() {
		        			if (dialog.fire('ok', { hide : true }).hide !== false) {
		        				dialog.hide();
		        			}
		        		}
		        	});
		        }
		    },
		    CKEDITOR.dialog.cancelButton
		],
		onCancel: function() {
			var dialog = this;
        	dialog.getParentEditor().setReadOnly(true);
		},
	};
} );