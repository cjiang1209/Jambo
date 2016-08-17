var RichTextEditor = (function() {
	return {
		render: function(id_component, config) {
			var editor = CKEDITOR.replace(id_component, {
				customConfig: config
			});

			// Return a RichTextEditor instance
			return (function(id_component) {
				var commentCache = {};
				
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
						evt.data.setContent(commentCache[commentId]);
					}
					else {
						var url = urlConfig.getComment + commentId + '/';
						$.get(url, function(data) {
							commentCache[commentId] = data;
							evt.data.setContent(data);
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
					console.log(id_component);
					var url = urlConfig.updateContent;
					$.post(url, {
						content: CKEDITOR.instances[id_component].getData()
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
							if (editor.name == id_component) {
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
					},
				}
			}(id_component));
		},
	}
})();