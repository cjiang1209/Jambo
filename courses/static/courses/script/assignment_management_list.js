$(document).ready(function () {
	var tmplNewStage = Handlebars.compile($("#new-stage-template").html());
	var tmplStage = Handlebars.compile($("#stage-template").html());
	
	$('.btn-add-stage').on('click', function () {
		var start_date = new Date();
		start_date.setDate(start_date.getDate() + 1);
		start_date.setHours(23);
		start_date.setMinutes(59);
		var end_date = new Date();
		end_date.setDate(end_date.getDate() + 8);
		end_date.setHours(23);
		end_date.setMinutes(59);
		var grace_period_end_date = end_date;
		
		var assignment = $(this).parent().find('input.hidden-assignment').val();
		
		var context = {
			assignment: assignment
		};
		var html = tmplNewStage(context);
		var tbody = $(this).parent().parent().find('table.table-stages tbody');
		tbody.append(html);
		
		tbody.find('form.form_new_stage input[name="start_date"]').datetimepicker({
			format: 'MM/DD/Y HH:mm',
			defaultDate: start_date
		});
		tbody.find('form.form_new_stage input[name="end_date"]').datetimepicker({
			format: 'MM/DD/Y HH:mm',
			defaultDate: end_date
		});
		tbody.find('form.form_new_stage input[name="grace_period_end_date"]').datetimepicker({
			format: 'MM/DD/Y HH:mm',
			defaultDate: grace_period_end_date
		});
	});
	
	$('.table-stages').on('submit', '.form_new_stage', function (evt) {
		evt.preventDefault();
		
		var form = $(this);
		var start_date = form.find('input[name="start_date"]').val();
		var end_date = form.find('input[name="end_date"]').val();
		var grace_period_end_date = form.find('input[name="grace_period_end_date"]').val();
		var assignment = form.find('input[name="assignment"]').val();
		
		$.post(urlAddStage, {
			start_date: start_date,
			end_date: end_date,
			grace_period_end_date: grace_period_end_date,
			assignment: assignment
		}).done(function (data) {
			var context = {
				id: data.id,
				start_date: start_date,
				end_date: end_date,
				grace_period_end_date: grace_period_end_date
			};
			var html = tmplStage(context);
			form.closest('tr').replaceWith(html);
		}).fail(function(data) {
			console.log(data);
		});
	});
	
	$('.table-stages').on('click', '.btn-cancel-add-stage', function (evt) {
		evt.preventDefault();
		$(this).closest('tr').remove();
	});
	
	$('.table-stages').on('click', '.btn-delete-stage', function (evt) {
		var tr = $(this).closest('tr');
		var stageId = tr.find('.hidden-stage').val();
		
		$.confirm({
			title: 'Delete a Stage',
			content: 'Please confirm to delete the stage.',
			backgroundDismiss: true,
			confirm: function() {
				var url = urlDeleteStage + stageId + '/';
				$.post(url, function (data) {
					tr.remove();
				});
			},
		});
	});
});