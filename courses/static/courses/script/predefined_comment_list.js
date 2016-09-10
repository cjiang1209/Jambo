var tmplAddCategory = Handlebars.compile($("#add-category-template").html());
var tmplAddCategoryLink = Handlebars.compile($("#add-category-link-template").html());
var tmplCategory = Handlebars.compile($("#category-template").html());
var tmplCategoryList = Handlebars.compile($("#category-list-template").html());

function addCategory(obj)
{
	var reserved = $(obj).closest('.li-reserved');
	var title = reserved.find('input[name="title"]').val();
	var parent = reserved.find('input[name="parent"]').val();
	
	if (title == '') {
		// Cancel
		html = tmplAddCategoryLink({ parent: parent });
		reserved.html(html);
	}
	else {
		// Submit
		$.post(urlAddPredefinedCommentCategory, {
			title: title,
			parent: parent
		}).done(function (data) {
			var html = tmplCategory({
				id: data.id,
				title: title,
				is_terminal: false
			});
			reserved.before(html);
			
			html = tmplAddCategoryLink({ parent: parent });
			reserved.html(html);
		}).fail(function (data) {
			console.log(data);
		});
	}
}

function deleteCategory(obj)
{
	var category = $(obj).closest('.li-category');
	var category_id = category.find('input[name="category_id"]').val();
	$.confirm({
	    title: 'Confirm',
	    content: 'All the comments and sub-categories under this category will be deleted.',
	    backgroundDismiss: true,
	    confirm: function() {
	        $.post(urlPredefinedCommentCategoryDelete + category_id + '/', {
	        	pk: category_id
	        }).done(function () {
	        	if (category.hasClass('active')) {
	        		// Remove the list  of sub-categories
	        		category.closest('div.div-category').nextAll('div.div-category').remove();
	        	}
	        	category.remove();
	        })
	    }
	});
}

function terminateCategory(obj)
{	
	$.confirm({
		title: 'Mark as a Terminal',
		content: 'Mark the selected category as a terminal will remove all its sub-categories. This operation cannot be revoked.',
		backgroundDismiss: true,
		confirm: function() {			
			var category = $(obj).closest('.li-category');
			var category_id = category.find('input[name="category_id"]').val();
			$.post(urlPredefinedCommentCategoryTerminate + category_id + '/', {
				pk: category_id
			}).done(function() {
				category.find('input[name="is_terminal"]').val(true);
				category.find('button.btn-terminate-category').remove();
			});
		},
	});
}

function showCommentOfCategory(obj)
{
	var category = $(obj).closest('.li-category');
	var category_id = category.find('input[name="category_id"]').val();
	$.get(urlCommentOfPredefinedCommentCategory + category_id + '/').done(function (data) {
		$('#form_comment').find('input[name="predefinedcomment_id"]').val(data.id);
		CKEDITOR.instances[idRichTextEditor].setData(data.content);
		$('#form_comment').show();
	});
}

$(document).ready(function () {
	$('#div_select_category').on('click', '.btn-add-category-link', function (evt) {
		var reserved = $(this).closest('.li-reserved');
		var parent = reserved.find('input[name="parent"]').val();
		var html = tmplAddCategory({ parent: parent });
		reserved.html(html);
		reserved.find('input[name="title"]').focus();
	});
	
	$('#div_select_category').on('focusout', '.form-add-category input[name="title"]', function (evt) {
		addCategory(this);
	});
	
	$('#div_select_category').on('click', '.link-show-subcategory', function (evt) {
		var category = $(this).closest('.li-category');
		category.siblings().removeClass('active');
		category.addClass('active');
		var div = $(this).closest('div.div-category');
		div.nextAll('div.div-category').remove();
		
		var category_id = category.find('input[name="category_id"]').val();
		var is_terminal = (category.find('input[name="is_terminal"]').val() == 'true');
		
		if (is_terminal) {
			showCommentOfCategory(this);
		}
		else {
			$.get(urlPredefinedCommentSubCategoryList + category_id + '/').done(function (data) {
				var html = tmplCategoryList({ parent: category_id, categories: data.list });
				div.after(html);
			});
			$('#form_comment').hide();
		}
	});
	
	$('#div_select_category').on('click', '.btn-terminate-category', function (evt) {
		evt.stopPropagation();
		terminateCategory(this);
	});
	
	$('#div_select_category').on('click', '.btn-delete-category', function (evt) {
		evt.stopPropagation();
		deleteCategory(this);
	});
	
	$('#form_comment').on('submit', function (evt) {
		evt.preventDefault();
		
		CKEDITOR.instances[idRichTextEditor].updateElement();
		
		var form = $(this);
		var comment_id = form.find('input[name="predefinedcomment_id"]').val();
		var content = form.find('textarea[name="content"]').val();
		
		$.post(urlPredefinedCommentUpdate + comment_id + '/', {
			content: content
		}).done(function (data) {
			$.alert({
			    title: 'Updated',
			    content: 'Predefined comment updated successfully.',
			    backgroundDismiss: true
			});
		});
	});
	
	var editorConfig = RichTextEditorConfig.EditComment();	
	var editor = RichTextEditor.render(idRichTextEditor, editorConfig);
	
	$('#form_comment').hide();
});