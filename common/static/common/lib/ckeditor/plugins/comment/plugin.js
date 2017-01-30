(function() {
	var pluginName = 'comment';
	var iconClass = 'cke_comment_icon';
	var idClass = 'cke_comment_id';
	var template = new CKEDITOR.template('<span>'
		+ '<span class="' + idClass + '">{comment_id}</span>'
		+ '<img class="' + iconClass + '" />'
		+ '</span>');
	
	var addCommentCmd = {
		canUndo : false,
		readOnly : true,
		exec : function(editor) {
			var sel = editor.getSelection();
			if (sel.getRanges().length > 0) {
				var range = sel.getRanges()[0];
				range.setEnd(range.startContainer, range.startOffset);
				sel.selectRanges([range]);
			}
			
			editor.setReadOnly(false);
			editor.execCommand(pluginName);
		}
	};
	
	var removeCommentCmd = {
		canUndo : false,
		readOnly : true,	
		exec : function(editor) {
			editor.setReadOnly(false);
			var widget = editor.widgets.selected[0];
			removeCommand(editor, widget);
			editor.setReadOnly(true);
			
			widget.fire('remove');
		}
	};
	
//	var hideCommentWindowCmd = {
//		canUndo : false,
//		readOnly : true,
//		exec : function(editor) {
//			tooltip.hide();
//		}
//	};
	
	function removeCommand(editor, widget) {
		editor.widgets.del(widget);
	}

	function tryRestoreCommentElement(editor, element) {
		if (element && element.type == CKEDITOR.NODE_ELEMENT && element.hasAttribute('data-cke-widget-wrapper')) {
			var child = element.getChild(0);
			if (child && child.hasAttribute('data-widget') && child.getAttribute('data-widget') == 'comment') {
				return child;
			}
		}
	}

	var plugin = {
	    requires: 'widget,dialog',
	    icons: 'comment',
	    draggable: false,
	    
	    onLoad: function() {
			var iconPath = CKEDITOR.getUrl( this.path + 'icons/comment.png' );
			var baseStyle = 'background:url(' + iconPath + ') no-repeat center;border:1px dotted #00f;background-size:16px;'
				+ 'width:16px;min-height:15px;height:1.15em;vertical-align:text-bottom;';
	    	
	    	CKEDITOR.addCss('.' + idClass + '{display:none}');
			CKEDITOR.addCss('.' + iconClass + '{' + baseStyle + '}');
//			CKEDITOR.document.appendStyleText( CKEDITOR.config.devtools_styles ||
//					'#cke_tooltip { max-width: 400px; }');
//			CKEDITOR.document.appendStyleText( CKEDITOR.config.devtools_styles ||
//				'#cke_tooltip { padding: 5px; border: 2px solid #333; background: #ffffff }' +
//				'#cke_tooltip h2 { font-size: 1.1em; border-bottom: 1px solid; margin: 0; padding: 1px; }' +
//				'#cke_tooltip ul { padding: 0pt; list-style-type: none; }' );
		},
	    
	    init: function(editor) {
	    	CKEDITOR.dialog.add('commentDialog', this.path + 'dialogs/comment.js');

	        editor.widgets.add(pluginName, {
	        	dialog: 'commentDialog',
	            template: template.output({
	            	comment_id: '',
	            }),
	            
	            parts: {
	            	comment_id: 'span.' + idClass,
	                icon: 'img.' + iconClass
	            },

	            //allowedContent: 'span(!' + cls + ')',
	            //requiredContent: 'span(!' + cls + ')',
	            
//	            upcast: function(element) {
//	                return element.name == 'span' && element.hasClass(cls);
//	            },
	            downcast: function() {
	            	return new CKEDITOR.htmlParser.text('[[[[' + this.data.comment_id + ']]]]');
	            },
	            
	            init: function() {
	            	this.setData('comment_id', this.parts.comment_id.getText());
	            	
	            	var widget = this;
	            	
	            	widget.parts.icon.on('mouseover', function(evt) {
	            		var cpos = editor.container.getDocumentPosition();
	            		var wpos = editor.window.getScrollPosition();
	            		var pos = widget.parts.icon.getDocumentPosition();
            		
            			widget.fire('mouseover', {
            				top: cpos.y - wpos.y + pos.y + 5,
            				left: cpos.x - wpos.x + pos.x + 5
            			});
	            	});

	            	widget.on('ready', function(evt) {
	            		editor.setReadOnly(true);
	            	});
	            },
	            
	            data: function() {
	            	this.parts.comment_id.setText(this.data.comment_id);
	            }
	        });
	        
	        editor.addCommand('addComment', addCommentCmd);
	        editor.addCommand('removeComment', removeCommentCmd);
	        
	        if (editor.contextMenu) {
	        	editor.addMenuGroup('comment');
	        	editor.addMenuItem('insertComment', {
					label: 'Insert Comment',
					icon: this.path + 'icons/comment.png',
					command: 'addComment',
					group: 'comment'
				});
				editor.addMenuItem('removeComment', {
					label: 'Remove Comment',
					icon: this.path + 'icons/comment.png',
					command: 'removeComment',
					group: 'comment'
				});
				
				editor.contextMenu.addListener(function (element) {
					var comment = tryRestoreCommentElement(editor, element);
					if (comment) {
						return {'removeComment': CKEDITOR.TRISTATE_OFF };
					}
					else {
						return {'insertComment': CKEDITOR.TRISTATE_OFF };
					}
				});
			}
	        
	        editor.ui.addButton('AddComment', {
				label: 'Add Comment',
				command: 'addComment',
				toolbar: 'insert',
				icon: 'comment'
			} );
	    },
	    
		afterInit: function(editor) {
			var commentRegex = /\[\[\[\[([^\[\]])+\]\]\]\]/mg;
			editor.dataProcessor.dataFilter.addRules({
				text: function(text, node) {
					var dtd = node.parent && CKEDITOR.dtd[node.parent.name];

					// Skip the case when placeholder is in elements like <title> or <textarea>
					// but upcast placeholder in custom elements (no DTD).
					if (dtd && !dtd.span)
						return;
					
					return text.replace(commentRegex, function(str) {					
						var regex = /\[\[\[\[(([^\[\]])+)\]\]\]\]/mg;
						var match = regex.exec(str);
						
						var innerElement = CKEDITOR.dom.element.createFromHtml(template.output({
							comment_id: match[1],
						}));

						var widgetWrapper = editor.widgets.wrapElement(innerElement, 'comment');
						// Return outerhtml of widget wrapper so it will be placed
						// as replacement.
						return widgetWrapper.getOuterHtml();
					} );
				}
			} );
		}
	};

	// Register a plugin.
	CKEDITOR.plugins.add(pluginName, plugin);
})();
