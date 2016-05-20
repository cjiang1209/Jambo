(function() {
	var pluginName = 'comment';
	var cls = 'cke_comment';
	var idCls = 'cke_comment_id';
	var template = new CKEDITOR.template('<span>'
		+ '<span class="' + idCls + '">{comment_id}</span>'
		+ '<span class="' + cls + '">{name}</span>'
		+ '</span>');
	var tooltipTemplate = new CKEDITOR.template('<span>{comment_id}</span>'
		+ '<span>{content}</span>'
		+ '<span>{create_date}</span>');
	
	var addCommentCmd = {
		canUndo : false,
		readOnly : true,
		exec : function(editor) {
			editor.setReadOnly(false);
			
			
			console.log(editor.getSelection().getStartElement());
			var ranges = editor.getSelection().getRanges();
			console.log(ranges.length);
			console.log(ranges);
			
			
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
	
	function showTooltip(widget, editor) {
		var cpos = editor.container.getDocumentPosition();
		var wpos = editor.window.getScrollPosition();
		var pos = widget.parts.name.getDocumentPosition();
		var styles = {
			'z-index': editor.config.baseFloatZIndex + 10,
			top: (cpos.y - wpos.y + pos.y + widget.parts.name.getSize('height') + 40) + 'px',
			left: (cpos.x - wpos.x + pos.x) + 'px'
		};

		tooltip.setStyles(styles);
		tooltip.show();
	}
	
	function hideTooltip(widget, editor) {
		tooltip.hide();
	}
	
	function getComment(widget, editor) {
		return widget.data.comment_id + ' - This is your comment';
	}
	
	function setTooltipContent(data) {
		tooltip.setCustomData('comment_id', data.comment_id);
		tooltip.setCustomData('content', data.content);
		tooltip.setCustomData('create_data', data.create_date);
		
		var html = tooltipTemplate.output({
        	comment_id: data.comment_id,
        	content: data.content,
        	create_date: data.create_date
        });
		tooltip.setHtml(html);
	}
	
	var plugin = {
	    requires: 'widget,dialog',
	    icons: 'comment',
	    draggable: false,
	    
	    onLoad: function() {
	    	CKEDITOR.addCss('.' + idCls + '{display:none}');
			CKEDITOR.addCss('.' + cls + '{background-color:#ff0}');
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
		    	tooltip.setCustomData('updating', false);
				tooltip.hide();
				tooltip.appendTo(editor.element.getParent());
	    	}
	    	
	        editor.widgets.add(pluginName, {
	        	dialog: 'comment',
	            //button: 'Add Comment',
	            template: template.output({
	            	comment_id: '',
	            	name: ''
	            }),
	            
	            parts: {
	            	comment_id: 'span.' + idCls,
	                name: 'span.' + cls
	            },

	            //allowedContent: 'span(!' + cls + ')',
	            //requiredContent: 'span(!' + cls + ')',
	            
//	            upcast: function(element) {
//	                return element.name == 'span' && element.hasClass(cls);
//	            },
	            downcast: function() {
	            	return new CKEDITOR.htmlParser.text('[[' + this.data.comment_id + ']]{{' + this.data.name + '}}');
	            },
	            
	            init: function() {
	            	this.setData('comment_id', this.parts.comment_id.getText());
	            	this.setData('name', this.parts.name.getHtml());
	            	
	            	var widget = this;
	            	this.parts.name.on('mouseover', function() {
	            		var id = widget.data.comment_id;
	            		if(id != tooltip.getCustomData('comment_id')) {
	            			tooltip.setCustomData('comment_id', id);
	            			tooltip.setCustomData('updating', true);
	            			widget.fire('showTooltip', {
	            				setContent: function(data) {
	            					setTooltipContent(data);
	            					showTooltip(widget, editor);
	            					tooltip.setCustomData('updating', false);
	            				}
	            			});
	            		}
	            		else{
	            			if(!tooltip.getCustomData('updating')) {
	            				showTooltip(widget, editor);
	            			}
	            		}
	            	});
	            	this.parts.name.on('mouseout', function() {
	            		hideTooltip(widget, editor);
	            	});
	            	this.on('select', function() {
	            		console.log('selected');
	            	});
	            	
	            	this.on('contextMenu', function(evt) {
	            		evt.data.removeComment = CKEDITOR.TRISTATE_OFF;
	            	});
	            	this.on('ready', function(evt) {
	            		editor.setReadOnly(true);
	            	});
	            },
	            
	            data: function() {
	            	this.parts.comment_id.setText(this.data.comment_id);
	            	this.parts.name.setHtml(this.data.name);
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
			var commentRegex = /\[\[([^\[\]])+\]\]{{([^{{])+}}/mg;
			editor.dataProcessor.dataFilter.addRules({
				text: function(text, node) {
					var dtd = node.parent && CKEDITOR.dtd[node.parent.name];

					// Skip the case when placeholder is in elements like <title> or <textarea>
					// but upcast placeholder in custom elements (no DTD).
					if (dtd && !dtd.span)
						return;
					
					return text.replace(commentRegex, function(str) {
						console.log(str);
						
						var regex = /\[\[(([^\[\]])+)\]\]{{(([^{{])+)}}/mg;
						var match = regex.exec(str);
						console.log(match[1]);
						console.log(match[3]);
						
						var innerElement = CKEDITOR.dom.element.createFromHtml(template.output({
							comment_id: match[1],
							name: match[3]
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
