$(function(){
	$(".clickable").click(function() {
		window.location = $(this).data("href");
	});
	$("form").submit(function(e){
	    e.preventDefault();
        e.stopImmediatePropagation();
        var inputted = $("#input").val();
	    if (inputted.length < 1){
	        window.location.replace("/");
        }
	    var url = "/all/" + inputted;
	    window.location.replace(url);
	});
});


