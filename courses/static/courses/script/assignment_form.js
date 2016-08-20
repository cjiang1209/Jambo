$(document).ready(function () {
	var tmplNewSubmissionPeriod = Handlebars.compile($("#new-submission-period-template").html());
	var tmplSubmissionPeriod = Handlebars.compile($("#submission-period-template").html());
	
	$('#btn_add_submission_period').on('click', function () {
		console.log('Add submission period');
		
		var start_date = new Date();
		start_date.setDate(start_date.getDate() + 1);
		var end_date = new Date();
		end_date.setDate(end_date.getDate() + 8);
		
		var context = {
			start_date: start_date.toLocaleString(),
			end_date: end_date.toLocaleString()
		};
		var html = tmplNewSubmissionPeriod(context);
		$('#list_submission_periods').append(html);
		
		$('form.form_new_submission_period input[name="start_date"]').datetimepicker({
			format: 'MM/DD/Y HH:mm'
		});
		$('form.form_new_submission_period input[name="end_date"]').datetimepicker({
			format: 'MM/DD/Y HH:mm'
		});
	});
	
//	$('#list_submission_periods').on('click', 'li form .cls_btn_confirm_add_submision_period', function(evt) {
//		console.log('Confirm submission period');
//		console.log(assignmentId);
//		
//		var form = $(evt.target).parent();
//		var title = form.child('')
//		
//		$.post(urlAddSubmissionPeriod, {
//			title: 
//		});
//	});
	
	$('#list_submission_periods').on('submit', 'li form.form_new_submission_period', function (evt) {
		evt.preventDefault();
		
		var form = $(this);
		var title = form.find('input[name="title"]').val();
		var start_date = form.find('input[name="start_date"]').val();
		var end_date = form.find('input[name="end_date"]').val();
		
		$.post(urlAddSubmissionPeriod, {
			title: title,
			start_date: start_date,
			end_date: end_date,
			assignment: assignmentId
		}).done(function (data) {
			var context = {
				id: data.id,
				title: title,
				start_date: start_date,
				end_date: end_date
			};
			var html = tmplSubmissionPeriod(context);
			form.parent().replaceWith(html);
		}).fail(function(data) {
			console.log(data);
		});
	});
	
	$('#list_submission_periods').on('click', 'li form .cls_btn_cancel_add_submision_period', function (evt) {
		$(evt.target).parent().parent().remove();
	});
	
	$('#list_submission_periods').on('click', 'li .cls_btn_delete_submission_period', function (evt) {
		var li = $(this).parent().parent();
		var periodId = li.find('.cls_hidden_submission_period_id').val();
		console.log("Delete Period " + periodId);
		
		var url = urlDeleteSubmissionPeriod + periodId + '/';
		$.post(url, function (data) {
			li.remove();
		});
	});
});