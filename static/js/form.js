$(function(){

	var email_pattern = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;

	$('#order').click(function(){
	    $("#error").html("");

	    if ($("#inputName").val().length < 1){
	        $("#error").html("Täitke oma nimi");
	        return;
        }

        if ($("#inputEmail").val().length < 4){
	        $("#error").html("Email on vale");
	        return;
        }

        if ($("#inputTelefon").val().length < 3){
	        $("#error").html("Telefon on liiga lühike");
	        return;
        }

        if ($("#inputKood").val().length < 3){
	        $("#error").html("Isikukood on vale");
	        return;
        }

		$.ajax({
			url: '/order',
			data: $('form').serialize(),
			type: 'POST',
			success: function(response){
				console.log(response);
				if (JSON.parse(response).hasOwnProperty("error")){
					swal({
						title: "Oops!",
						text: "Niisugust raamatut ei ole",
						icon: "error",
						button: "Lõpeta"
					}).then(function(){
				    	window.location.href = "/"
					});
				} else{
					swal({
						title: "Hurrah!",
						text: "Raamat on edukalt laenatud",
						icon: "success",
						button: "Lõpeta"
					}).then(function(){
				    	window.location.href = "/"
					});
				}


			},
			error: function(error){
				console.log(error);
				$("#error").html(error);
			}
		});
	});
});


