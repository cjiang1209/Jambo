(function() {
//	var commentCmd = {
//		canUndo : false,
//		readOnly : true,	
//		exec : function(editor) {
//			var style = new CKEDITOR.style({
//			    element : 'span',
//			    attributes : {
//			    	'class' : 'marker'
//			    }
//			});
//			
//			if(editor.readOnly) {
//				editor.setReadOnly(false);
//				editor.applyStyle(style);
//				editor.setReadOnly(true);
//			}
//			else {
//				editor.applyStyle(style);
//			}
//			
//			editor.fire('add_comment', 2);
//		}
//	};

	var pluginName = 'comment';
	
	var widget = {
	    requires: 'widget',
	    icons: 'comment',
	    draggable: false,
	    inline: true,
	    mask: true,
	    init: function(editor) {
	    	var cls = 'comment';
	        editor.widgets.add(pluginName, {
	            button: 'Add Comment',
	            template: '<span class="' + cls + '"></span>',
	            
	            parts: {
	                comment: 'span.' + cls
	            },

	            allowedContent: 'span(!' + cls + ')',
	            
	            upcast: function(element) {
	                return element.name == 'span' && element.hasClass(cls);
	            },
	            
	            init: function() {
	            	var content = this.parts.comment.getChild(0);
	            	if(!content) {
		            	var html = editor.getSelectedHtml(true);
		            	this.parts.comment.appendHtml(html);
	            	}
	            }
	        });
	    }
	};

	// Register a plugin.
	CKEDITOR.plugins.add(pluginName, widget);
//	CKEDITOR.plugins.add(pluginName, {
//		init : function(editor) {
//			editor.addCommand(pluginName, commentCmd);
//		}
//	});
})();
