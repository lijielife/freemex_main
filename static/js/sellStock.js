$(function() {
	console.log("SellStock: ready");
    $('.fallbackJS').hide();
    console.log("SellStock: all fallbackJS hidden");
    $('.JS').show();
    console.log("BuyStock: all JS show");


    $('.sellJsButton').click(
    	function(e){
	    	e.preventDefault();
	    	var a = $(this);
	    	var stockname = a.data("stockname");
	    	var stockcode = a.data("stockcode");
	    	var qty = a.data("stockqty");
	    	console.log("selling " + stockname + " " + stockcode);
	    	var box = $('#sell-lightbox');
	    	$('#sell-lightboxStockname').html(stockname);
	    	$('#sell-lightboxStockcode').html(stockcode);
	    	$('#sell-lightboxStockcode2').val(stockcode);
    		var boxbg = $('#sell-lightboxbg').fadeIn();
    		box.fadeIn();
    		}
    		);
    $('#sell-crossLightbox').click(
    	function(e){
    		$('#sell-lightbox').fadeOut();
    		$('#sell-lightboxbg').fadeOut();
    	}
    	);

    $('#sell-lightboxbg').click(
    	function(e){
    		$('#sell-lightbox').fadeOut();
    		$(this).fadeOut();
    	}
    	);

});