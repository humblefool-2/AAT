$(document).ready(function(){
	$('#btnSignUp').click(function(){
		
		$.ajax({
			url: '/sp_page',
			data: $('form').serialize(),
			type: 'POST',
			success: function(response)  //response stores string returned from app.py
			{
				
				console.log(response);  //prints string on browser console
			},
			error: function(error){
				console.log(error);  //prints string on browser console in case of error
			}
		});
	});
});