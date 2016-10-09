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
				
				var htmlTmplComment = 
					'<div class="panel-heading draggable-heading">' +
					'<span>{{create_date}}</span>' +
					'<span><button type="button" class="close cls_btn_close" aria-label="Close"><span aria-hidden="true">&times;</span></button></span>' +
					'</div>' +
					'<div class="panel-body">{{{content}}}</div>';
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
				
				var showCommentPopup = function (evt) {
					var widget = evt.sender;
					var commentId = widget.data.comment_id;
					if (commentCache.hasOwnProperty(commentId)) {
						var popup = $('#div_comment_popup');
						popup.html(tmplComment(commentCache[commentId]));
						popup.css({
							left: evt.data.left,
							top: evt.data.top + 60
						});
						popup.show();
					}
					else {
						var url = urlConfig.getComment + commentId + '/';
						$.get(url, function(data) {
							commentCache[commentId] = data;
							
							var popup = $('#div_comment_popup');
							popup.html(tmplComment(data));
							popup.css({
								left: evt.data.left,
								top: evt.data.top + 60
							});
							popup.show();
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
										widget.on('mouseover', showCommentPopup);
										
										if (!readonly) {
											widget.on('remove', removeComment);
										}
									}
								});
								
								if (!readonly) {
									editor.widgets.on('instanceCreated', function(evt) {
										var widget = evt.data;
										if (widget.name == 'comment') {
											widget.on('mouseover', showCommentPopup);
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
						
						//CKEDITOR.instances[id_content].element.getParent().appendHtml('<div id="div_comment_popup" class="panel panel-primary" style="position: absolute; z-index: 200;"></div>');
						$('body').append('<div id="div_comment_popup" class="panel panel-primary comment-popup"></div>');
						var popup = $('#div_comment_popup').draggable();
						popup.on('click', '.cls_btn_close', function () {
							//editor.execCommand('hideCommentWindow');
							$('#div_comment_popup').hide();
						});
						popup.draggable();
						popup.hide();
					},
				};
			}(id_content));
		},
	};
})();
