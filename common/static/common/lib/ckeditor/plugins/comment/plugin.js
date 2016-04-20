(function() {
	var removeCommentCmd = {
		canUndo : false,
		readOnly : true,	
		exec : function(editor) {
			console.log('Remove command');
		}
	};
	
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

	var pluginName = 'comment';
	
	var plugin = {
	    requires: 'widget,dialog',
	    icons: 'comment',
	    draggable: false,
	    
	    onLoad: function() {
			// Register styles for placeholder widget frame.
			CKEDITOR.addCss('.cke_comment{background-color:#ff0}');
		},
	    
	    init: function(editor) {
	    	CKEDITOR.dialog.add('comment', this.path + 'dialogs/comment.js');
	    	
	    	if (!tooltip) {
		    	tooltip = CKEDITOR.dom.element.createFromHtml(
		    			'<div id="cke_tooltip" tabindex="-1" style="position: absolute"></div>',
		    			CKEDITOR.document);
				tooltip.hide();
				tooltip.on('mouseover', function() {
					this.show();
				});
				tooltip.on('mouseout', function() {
					this.hide();
				});
				//tooltip.appendTo(CKEDITOR.document.getBody());
				tooltip.appendTo(editor.element.getParent());
	    	}
	    	
	    	var cls = 'cke_comment';
	        editor.widgets.add(pluginName, {
	        	dialog: 'comment',
	            button: 'Add Comment',
	            template: '<span class="' + cls + '"></span>',
	            
	            parts: {
	                comment: 'span.' + cls
	            },

	            allowedContent: 'span(!' + cls + ')',
	            //requiredContent: 'span(!' + cls + ')',
	            
	            upcast: function(element) {
	                return element.name == 'span' && element.hasClass(cls);
	            },
//	            downcast: function() {
//	            	return new CKEDITOR.htmlParser.text(this.data.name);
//	            },
	            
	            init: function() {
//	            	var content = this.parts.comment.getChild(0);
//	            	if(!content) {
//		            	var html = editor.getSelectedHtml(true);
//		            	this.parts.comment.appendHtml(html);
//	            	}
	            	var html = editor.getSelectedHtml(true);
	            	this.setData('name', html);
	            	this.parts.comment.on('mouseover', function() {
	            		showTooltip(getComment, this, editor);
	            	});
	            	this.parts.comment.on('mouseout', function() {
	            		hideTooltip(getComment, this, editor);
	            	});
	            	
	            	this.on('contextMenu', function(evt) {
	            		evt.data.removeComment = CKEDITOR.TRISTATE_OFF;
	            	});
	            },
	            
	            data: function() {
	            	this.parts.comment.appendHtml(this.data.name);
	            }
	        });
	        
	        if (editor.contextMenu) {
	        	editor.addCommand('removeComment', removeCommentCmd);
	        	
	        	editor.addMenuGroup('comment');
				editor.addMenuItem('removeComment', {
					label: 'Remove Comment',
					icon: this.path + 'icons/comment.png',
					command: 'removeComment',
					group: 'comment'
				});
			}
	    }
	};

	// Register a plugin.
	CKEDITOR.plugins.add(pluginName, plugin);
})();
