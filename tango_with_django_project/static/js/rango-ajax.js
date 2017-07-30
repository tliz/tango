$('#likes').click(function(){
	var catid;
	catid = $(this).attr("data-catid");
	$.get('/rango/like/', {category_id: catid}, function(data){
		$('#like_count').html(data);
			$('#likes').hide();
	}); 
});

$('#suggestion').keyup(function(){
	var query;
	query = $(this).val();
	$.get('/rango/suggest/', {suggestion: query}, function(data){
		$('#cats').html(data);
	});
});

// Submit page on submit
$('#page-form').on('submit', function(event){
    event.preventDefault();
    console.log("form submitted!")  // sanity check
    create_page();
});

// AJAX for posting
function create_page() {
    console.log("create page is working!") // sanity check
    console.log($('#page-text').val())
};



