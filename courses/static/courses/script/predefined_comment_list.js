$(document).ready(function () {
	var tmplAddCategory = Handlebars.compile($("#add-category-template").html());
	var tmplAddCategoryLink = Handlebars.compile($("#add-category-link-template").html());
	var tmplCategory = Handlebars.compile($("#category-template").html());
	var tmplCategoryList = Handlebars.compile($("#category-list-template").html());
	
	$('#div_select_category').on('click', '.btn-add-category-link', function (evt) {
		var reserved = $(this).closest('li.li-reserved');
		var parent = reserved.find('input[name="parent"]').val();
		var html = tmplAddCategory({ parent: parent });
		reserved.html(html);
		reserved.find('input[name="title"]').focus();
	});
	
	$('#div_select_category').on('focusout', '.form-add-category input[name="title"]', function (evt) {
		var reserved = $(this).closest('li.li-reserved');
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
					title: title
				});
				reserved.before(html);
				
				html = tmplAddCategoryLink({ parent: parent });
				reserved.html(html);
			}).fail(function (data) {
				console.log(data);
			});
		}
	});
	
	$('#div_select_category').on('click', '.link-show-subcategory', function (evt) {
		var div = $(this).closest('div.div-category');
		div.nextAll('div.div-category').remove();
		
		var html = tmplCategoryList();
		div.after(html);
	});
});