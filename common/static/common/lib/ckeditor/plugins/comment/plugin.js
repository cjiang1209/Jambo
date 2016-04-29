(function() {
	var pluginName = 'comment';
	var cls = 'cke_comment';
	
	var addCommentCmd = {
		canUndo : false,
		readOnly : true,
		exec : function(editor) {
			editor.setReadOnly(false);
			editor.execCommand(pluginName);
		}
	};
	
	var removeCommentCmd = {
		canUndo : false,
		readOnly : true,	
		exec : function(editor) {
			editor.setReadOnly(false);
			removeCommand(editor, editor.widgets.selected[0]);
			editor.setReadOnly(true);
		}
	};
	
	function removeCommand(editor, widget) {
		editor.insertHtml(widget.data.name);
		//editor.widgets.del(widget);
	}
	
	var tooltip;
	
	function showTooltip(callback, el, editor) {
		var cpos = editor.container.getDocumentPosition();
		var wpos = editor.window.getScrollPosition();
		var pos = el.getDocumentPosition();
		var styles = { 'z-index': editor.config.baseFloatZIndex + 10,
			top: (cpos.y - wpos.y + pos.y + el.getSize( 'height' )) + 'px',
			left: (cpos.x - wpos.x + pos.x) + 'px' };

		tooltip.setHtml(callback(el, editor));
		tooltip.setStyles(styles);
		tooltip.show();
	}
	
	function hideTooltip(callback, el, editor) {
		tooltip.hide();
	}
	
	function getComment(el, editor) {
		return 'This is your comment';
	}
	
	var plugin = {
	    requires: 'widget,dialog',
	    icons: 'comment',
	    draggable: false,
	    
	    onLoad: function() {
			CKEDITOR.addCss('.cke_comment{background-color:#ff0}');
			CKEDITOR.document.appendStyleText( CKEDITOR.config.devtools_styles || '#cke_tooltip { padding: 5px; border: 2px solid #333; background: #ffffff }' +
				'#cke_tooltip h2 { font-size: 1.1em; border-bottom: 1px solid; margin: 0; padding: 1px; }' +
				'#cke_tooltip ul { padding: 0pt; list-style-type: none; }' );
		},
	    
	    init: function(editor) {
	    	CKEDITOR.dialog.add('comment', this.path + 'dialogs/comment.js');
	    	
	    	if (!tooltip) {
		    	tooltip = CKEDITOR.dom.element.createFromHtml(
		    			'<div id="cke_tooltip" tabindex="-1" style="position: absolute"></div>',
		    			CKEDITOR.document);
				tooltip.hide();
//				tooltip.on('mouseover', function() {
//					this.show();
//				});
//				tooltip.on('mouseout', function() {
//					this.hide();
//				});
				//tooltip.appendTo(CKEDITOR.document.getBody());
				tooltip.appendTo(editor.element.getParent());
	    	}
	    	
	        editor.widgets.add(pluginName, {
	        	dialog: 'comment',
	            //button: 'Add Comment',
	            template: '<span class="' + cls + '"></span>',
	            
	            parts: {
	                comment: 'span.' + cls
	            },

	            //allowedContent: 'span(!' + cls + ')',
	            //requiredContent: 'span(!' + cls + ')',
	            
//	            upcast: function(element) {
//	                return element.name == 'span' && element.hasClass(cls);
//	            },
	            downcast: function() {
	            	return new CKEDITOR.htmlParser.text('{{' + this.data.name + '}}');
	            },
	            
	            init: function() {
	            	this.setData('name', this.parts.comment.getHtml());
	            	
	            	this.parts.comment.on('mouseover', function() {
	            		showTooltip(getComment, this, editor);
	            	});
	            	this.parts.comment.on('mouseout', function() {
	            		hideTooltip(getComment,  this, editor);
	            	});
	            	
	            	this.on('contextMenu', function(evt) {
	            		evt.data.removeComment = CKEDITOR.TRISTATE_OFF;
	            	});
	            	this.on('ready', function(evt) {
	            		editor.setReadOnly(true);
	            	});
	            },
	            
	            data: function() {
	            	this.parts.comment.setHtml(this.data.name);
	            }
	        });
	        
	        editor.addCommand('addComment', addCommentCmd);
	        editor.addCommand('removeComment', removeCommentCmd);
	        
	        if (editor.contextMenu) {
	        	editor.addMenuGroup('comment');
				editor.addMenuItem('removeComment', {
					label: 'Remove Comment',
					icon: this.path + 'icons/comment.png',
					command: 'removeComment',
					group: 'comment'
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
			var commentReplaceRegex = /{{([^{{])+}}/g;
			editor.dataProcessor.dataFilter.addRules({
				text: function(text, node) {
					var dtd = node.parent && CKEDITOR.dtd[node.parent.name];

					// Skip the case when placeholder is in elements like <title> or <textarea>
					// but upcast placeholder in custom elements (no DTD).
					//if (dtd && !dtd.span)
					//	return;

					return text.replace(commentReplaceRegex, function(match) {
						console.log(match);
						
						// Creating widget code
						var innerElement = new CKEDITOR.htmlParser.element('span', {
							'class': cls
						});

						innerElement.add(new CKEDITOR.htmlParser.text(match.substring(2, match.length-2)));
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
