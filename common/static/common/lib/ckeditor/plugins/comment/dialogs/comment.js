CKEDITOR.dialog.add('comment', function(editor) {
	return {
		title: 'Comment',
		minWidth: 500,
		minHeight: 200,
		contents: [
			{
				id: 'cke_info',
				label: 'Comment',
				title: 'Comment',
				elements: [
					// Dialog window UI elements.
					{
						//id: 'cke_content',
						type: 'textarea',
						id: 'cke_content',
						style: 'width: 100%;',
						label: 'Your comment',
						'default': '',
						required: true,
						onLoad: function(widget) {
							CKEDITOR.replace(this.getInputElement().getId());
						},
						commit: function(widget) {
							//widget.setData('name', this.getValue());
						}
					}
				]
			}
		]
	};
} );