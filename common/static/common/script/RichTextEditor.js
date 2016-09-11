var RichTextEditorConfig = (function() {
	return {
		Edit: function() {
			return {
				toolbarGroups: [
	        	    //{ name: 'basicstyles', groups: [ 'basicstyles', 'cleanup' ] },
	        	    { name: 'clipboard', groups: [ 'clipboard', 'undo' ] },
	        	    //{ name: 'paragraph', groups: [ 'list', 'indent', 'blocks', 'align', 'bidi', 'paragraph' ] },
	        	    //{ name: 'styles', groups: [ 'styles' ] },
	        	    { name: 'editing', groups: [ 'spellchecker'] },
	        	    //{ name: 'insert', groups: [ 'insert' ] },
	        	    //{ name: 'document', groups: [ 'mode', 'document', 'doctools' ] }
	        	],
	        	//extraPlugins: 'uploadimage,image2,html5audio',
	        	removePlugins: 'elementspath',
	        	//removeButtons: 'Subscript,Superscript,Styles,Blockquote',
	        	allowedContent: true,
	        	height: 500,
	        };
		},
		ReadOnly: function() {
			return {
				toolbarGroups: [
                    //{ name: 'basicstyles', groups: [ 'basicstyles', 'cleanup' ] },
	                { name: 'clipboard', groups: [ 'clipboard', 'undo' ] },
	                //{ name: 'paragraph', groups: [ 'list', 'indent', 'blocks', 'align', 'bidi', 'paragraph' ] },
	                //{ name: 'styles', groups: [ 'styles' ] },
	                { name: 'editing', groups: [ 'spellchecker'] },
	                //{ name: 'insert', groups: [ 'insert' ] },
	                //{ name: 'document', groups: [ 'mode', 'document', 'doctools' ] }
                ],
				removePlugins: 'elementspath',
				allowedContent: true,
				readOnly: true,
				//removeButtons: 'Subscript,Superscript,Styles,Blockquote',
				height: 500,
			};
		},
		Comment: function() {
			return {
				toolbarGroups: [
	                { name: 'insert', groups: [ 'insert' ] },
			        //{ name: 'document', groups: [ 'mode', 'document', 'doctools' ] }
			    ],
			    removePlugins: 'elementspath',
			    removeButtons: 'Image,Table,HorizontalRule,SpecialChar',
			    allowedContent: true,
			    readOnly: true,
			    extraPlugins: 'comment',
			    height: 400,
			};
		},
		EditComment: function() {
			return {
				toolbarGroups: [
	                { name: 'basicstyles', groups: [ 'basicstyles', 'cleanup' ] },
	        	    { name: 'clipboard', groups: [ 'clipboard', 'undo' ] },
	        	    { name: 'paragraph', groups: [ 'list', 'indent', 'blocks', 'align', 'bidi', 'paragraph' ] },
	        	    //{ name: 'styles', groups: [ 'styles' ] },
	        	    { name: 'editing', groups: [ 'spellchecker'] },
	        	    { name: 'insert', groups: [ 'insert' ] },
	        	    { name: 'colors', groups: [ 'colors' ] },
	        	    //{ name: 'document', groups: [ 'mode', 'document', 'doctools' ] }
			    ],
			    extraPlugins: 'uploadimage,image2,html5audio,colorbutton',
			    removePlugins: 'elementspath',
			    allowedContent: true,
			    // Upload URLs
				uploadUrl: '/courses/imageupload/',
				filebrowserBrowseUrl: '/courses/audiobrowse/',
				filebrowserImageBrowseUrl: '/courses/imagebrowse/',
				filebrowserUploadUrl: '/courses/audioupload/',
				filebrowserImageUploadUrl: '/courses/imageupload/',
			};
		},
		ReadOnlyComment: function() {
			return {
				toolbarGroups: [
                    //{ name: 'basicstyles', groups: [ 'basicstyles', 'cleanup' ] },
                    { name: 'clipboard', groups: [ 'clipboard', 'undo' ] },
                    //{ name: 'paragraph', groups: [ 'list', 'indent', 'blocks', 'align', 'bidi', 'paragraph' ] },
                    //{ name: 'styles', groups: [ 'styles' ] },
                    { name: 'editing', groups: [ 'spellchecker'] },
                    //{ name: 'insert', groups: [ 'insert' ] },
                    //{ name: 'document', groups: [ 'mode', 'document', 'doctools' ] }
				],
				removePlugins: 'elementspath',
				allowedContent: true,
				readOnly: true,
				extraPlugins: 'comment',
				removeButtons: 'Subscript,Superscript,Styles,Blockquote',
				height: 500,
			};
		},
	};
})();

var RichTextEditor = (function() {
	return {
		render: function(id_content, editorConfig) {
			var editor = CKEDITOR.replace(id_content, editorConfig);

			// Return a RichTextEditor instance
			return (function(id_content) {
				var commentCache = {};
				
				HandlebarsIntl.registerWith(Handlebars);
				
				var htmlTmplComment = '<div class="panel panel-primary">' +
					'<div class="panel-heading">' +
					'<span>{{formatTime create_date}}</span>' +
					'<span><button type="button" class="close cls_btn_close" aria-label="Close"><span aria-hidden="true">&times;</span></button></span>' +
					'</div>' +
					'<div class="panel-body">{{{content}}}</div>' +
					'</div>';
				var tmplComment = Handlebars.compile(htmlTmplComment);
				
				var urlConfig = {
					contentId: "",
					getComment: "",
					addComment: "",
					deleteComment: "",
					updateContent: "",
				};
				
				var addComment = function (evt) {
					var dialog = evt.sender;
					console.log('fire ok');
					$.post(urlConfig.addComment, {
						attempt: urlConfig.contentId,
						content: dialog.getValueOf('cke_info', 'cke_content')
					}, function(data) {
						dialog.setValueOf('cke_info', 'cke_comment_id', data.id);
						evt.data.success();
						updateContent();
					});
				};
				
				var setTooltipContent = function (evt) {
					var widget = evt.sender;
					var commentId = widget.data.comment_id;
					if (commentCache.hasOwnProperty(commentId)) {
						var html = tmplComment(commentCache[commentId]);
						evt.data.setContent(html);
					}
					else {
						var url = urlConfig.getComment + commentId + '/';
						$.get(url, function(data) {
							commentCache[commentId] = data;
							var html = tmplComment(data);
							evt.data.setContent(html);
						});
					}
				};
				
				var removeComment = function (evt) {
					console.log('Remove Comment');
					
				 	var widget = evt.sender;
				 	var commentId = widget.data.comment_id;
				 	console.log(commentId);
				 	delete commentCache[commentId];
				 	var url = urlConfig.deleteComment + commentId + '/';
				  	$.post(url, function(data) {
				 		updateContent();
				 	});
				};
				
				var updateContent = function () {
					console.log(id_content);
					var url = urlConfig.updateContent;
					$.post(url, {
						content: CKEDITOR.instances[id_content].getData()
					}, function(data) {
						console.log(data);
					})
				};

				return {
					supportComment: function(config, readonly) {
						if (urlConfig == undefined) {
							console.log("A URL config is required.");
							return;
						}
						
						urlConfig = config;
						
						if (!readonly) {
							CKEDITOR.on('dialogDefinition', function(evt) {
								if (evt.data.name == 'commentDialog') {
									var dialogDef = evt.data.definition;
									console.log('listen to commit comment');
									dialogDef.dialog.on('commitComment', addComment);
								}
							});
						}
						
						CKEDITOR.on('instanceReady', function(evt) {
							var editor = evt.editor;
							if (editor.name == id_content) {
								console.log(editor.title);

								$.each(editor.widgets.instances, function(index, value) {
									var widget = value;
									if (widget.name == 'comment') {
										console.log('listen to show tooltip');
										widget.on('showTooltip', setTooltipContent);
										
										if (!readonly) {
											widget.on('remove', removeComment);
										}
									}
								});
								
								if (!readonly) {
									editor.widgets.on('instanceCreated', function(evt) {
										var widget = evt.data;
										if (widget.name == 'comment') {
											console.log('listen to show tooltip');
											widget.on('showTooltip', setTooltipContent);
											widget.on('remove', removeComment);
										}
									});
								}
								else {
									editor.removeMenuItem('removeComment');
									//console.log(editor.ui.get('AddComment'));
									//editor.ui.get('AddComment').setState(CKEDITOR.TRISTATE_OFF);
								}
							}
						});
						
						$('body').on('click', '.cls_btn_close', function () {
							editor.execCommand('hideCommentWindow');
						});
					},
				};
			}(id_content));
		},
	};
})();