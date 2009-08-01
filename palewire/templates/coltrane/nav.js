
		// Pulls a random item from an array
		var random_item = function ( array ) {
			var n = array.length;
			return array[(Math.floor(Math.random() * n))];
		};
	
		// Add titles for link buttons
		jQuery.each($("#navbar a"), function() {
			var title = $( this ).attr("title");
			$('#hd h1').append('<span class="icon" title="'+ title + '">'+ title +'<\/span>');
		});
		
		// Hide newly created link titles
		$('#hd span').hide()
	
		// Show link title on mouseover
		$('#navbar a').mouseover(function(){
			var title = $(this).attr('title');
			$('#hd span[title='+title+']').show();
			})
		
		// Hide link title on mouseoff
		$('#navbar a').mouseout(function(){
			var title = $(this).attr('title');
			$('#hd span[title='+title+']').hide();
			})
