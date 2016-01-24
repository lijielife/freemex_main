$(function() {
    console.log("BuyStock: ready");
    $('.withoutJS').hide();
    console.log("BuyStock: all withoutJS hidden");
    $('.withJS').show();
    console.log("BuyStock: all withJS show");

    $('#lightboxbg').click(
    	function(e){
    		$('#lightbox').fadeOut();
    		$(this).fadeOut();
    	}
    	);

    $('#crossLightbox').click(
    	function(e){
    		$('#lightbox').fadeOut();
    		$('#lightboxbg').fadeOut();
    	}
    	);

    $('.buyJsButton').click(
    	function(e){
	    	e.preventDefault();
	    	var a = $(this);
	    	var stockname = a.data("stockname");
	    	var stockcode = a.data("stockcode");
	    	console.log("buying " + stockname + " " + stockcode);
	    	var box = $('#lightbox');
	    	$('#lightboxStockname').html(stockname);
	    	$('#lightboxStockcode').html(stockcode);
	    	$('#lightboxStockcode2').val(stockcode);
    		var boxbg = $('#lightboxbg').fadeIn();
    		box.fadeIn();
    		}
    		);

});