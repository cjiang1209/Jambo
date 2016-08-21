$(document).ready(function () {
	var tmplNewSubmissionPeriod = Handlebars.compile($("#new-submission-period-template").html());
	var tmplSubmissionPeriod = Handlebars.compile($("#submission-period-template").html());
	
	$('#btn_add_submission_period').on('click', function () {
		var start_date = new Date();
		start_date.setDate(start_date.getDate() + 1);
		start_date.setHours(23);
		start_date.setMinutes(59);
		var end_date = new Date();
		end_date.setDate(end_date.getDate() + 8);
		end_date.setHours(23);
		end_date.setMinutes(59);
		
		var assignment = $(this).parent().find('input.cls_hidden_assignment').val();
		
		var context = {
			assignment: assignment,
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
	
	$('#list_submission_periods').on('submit', 'li form.form_new_submission_period', function (evt) {
		evt.preventDefault();
		
		var form = $(this);
		var title = form.find('input[name="title"]').val();
		var start_date = form.find('input[name="start_date"]').val();
		var end_date = form.find('input[name="end_date"]').val();
		var assignment = form.find('input[name="assignment"]').val();
		
		$.post(urlAddSubmissionPeriod, {
			title: title,
			start_date: start_date,
			end_date: end_date,
			assignment: assignment
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
		
		var url = urlDeleteSubmissionPeriod + periodId + '/';
		$.post(url, function (data) {
			li.remove();
		});
	});
});