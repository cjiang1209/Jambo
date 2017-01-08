function syncEndDateAndGracePeriodEndDate() {
	var end_date = $('#inputEndDate').data('DateTimePicker').date();
	$('#inputGracePeriodEndDate').data('DateTimePicker').date(end_date);
}

function initializeModelAddStage() {
	$('#inputStartDate').datetimepicker({
		format: 'MM/DD/Y HH:mm',
		sideBySide: true
	});
	$('#inputEndDate').datetimepicker({
		format: 'MM/DD/Y HH:mm',
		sideBySide: true,
	});
	$('#inputGracePeriodEndDate').datetimepicker({
		format: 'MM/DD/Y HH:mm',
		sideBySide: true,
	});

	$('#modalAddStage').on('show.bs.modal', function (evt) {
		var start_date = new Date();
		start_date.setDate(start_date.getDate());
		start_date.setHours(23);
		start_date.setMinutes(59);
		var end_date = new Date();
		end_date.setDate(end_date.getDate() + 7);
		end_date.setHours(23);
		end_date.setMinutes(59);
		var grace_period_end_date = end_date;

		$('#inputStartDate').data('DateTimePicker').date(start_date);
		$('#inputEndDate').data('DateTimePicker').date(end_date);
		$('#inputGracePeriodEndDate').data('DateTimePicker').date(grace_period_end_date);

		$('#checkSyncEndDateAndGracePeriod').prop('checked', true);
		$('#inputGracePeriodEndDate').prop('readonly', true);
	});

	$('#checkSyncEndDateAndGracePeriod').change(function () {
		if (this.checked) {
			// Sync
			$('#inputGracePeriodEndDate').prop('readonly', true);
			syncEndDateAndGracePeriodEndDate();
		}
		else {
			// No sync
			$('#inputGracePeriodEndDate').prop('readonly', false);
		}
	});

	$('#inputEndDate').on('dp.change', function () {
		if ($('#checkSyncEndDateAndGracePeriod').prop('checked')) {
			syncEndDateAndGracePeriodEndDate();
		}
	});

	$('#formAddStage').submit(function (evt) {
		evt.preventDefault();

		var form = $(this);
		var start_date = $('#inputStartDate').val();
		var end_date = $('#inputEndDate').val();
		var grace_period_end_date = $('#inputGracePeriodEndDate').val();
		var assignment = $('#inputAssignment').val();

		$.post(urlAddStage, {
			start_date: start_date,
			end_date: end_date,
			grace_period_end_date: grace_period_end_date,
			assignment: assignment
		}).done(function (data) {
			location.reload();
		}).fail(function(response) {
			$.alert({
				title: 'Error',
				content: response.responseText
			});
		});
	});
}

$(document).ready(function () {
	initializeModelAddStage();

	$('.btn-add-stage').click(function (evt) {	
		$('#inputAssignment').val($(this).data('assignment'));
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