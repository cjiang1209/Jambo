var tmplCategoryList = Handlebars.compile($("#category-list-template").html());

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
	
	$('#form_comment').on('submit', function (evt) {
		evt.preventDefault();
		
		CKEDITOR.instances[idRichTextEditor].updateElement();
		
		var form = $(this);
		var content = form.find('textarea[name="content"]').val();
		window.opener.CKEDITOR.tools.callFunction(CKEditorFuncNum, content);
		window.close();
	});
	
	var editorConfig = RichTextEditorConfig.ReadOnly();	
	var editor = RichTextEditor.render(idRichTextEditor, editorConfig);
	
	$('#form_comment').hide();
});