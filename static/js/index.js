$(document).ready(function(){

	$('#submit_button').on('click',function(){
		  var first_month = $('#1_month').val();
		  var second_month = $('#2_month').val();
		  var third_month = $('#3_month').val();
		  var fourth_month = $('#4_month').val();
		  var fifth_month = $('#5_month').val();
		  var tmp_url = '/api/predict/'+first_month+'+'+second_month+'+'+third_month+'+'+fourth_month+'+'+fifth_month;

		  $.ajax({
		    type: 'GET',
		    url: tmp_url,
		    success: function (data) {
		      $('#cross_validation').text('The predicted next month saving account balance '+ data['change']+'; and the predicted saing account balance belongs to group: '
		      	+data['classification']+';' + data['suggest']);
		    }
		  });
	});
	


});