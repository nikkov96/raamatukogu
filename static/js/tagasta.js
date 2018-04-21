$(function(){
	$('#tagasta').click(function(){
	    $("#error").html("");

	    if ($("#inputTelefon").val().length < 1){
	        $("#error").html("Täitke oma nimi");
	        return;
        }

        if ($("#inputKood").val().length < 1){
	        $("#error").html("Täitke oma isikukood");
	        return;
        }

		$.ajax({
			url: '/tagasta',
			data: $('form').serialize(),
			type: 'POST',
			success: function(response){
				console.log(response);
				swal({
					title: "Hurrah!",
					text: "Raamat on edukalt tagastatud",
					icon: "success",
					button: "Lõpeta"
				}).then(function(){
				    window.location.href = "/"
				});
			},
			error: function(error){
				console.log(error);
				$("#error").html(error);
			}
		});
	});
});


