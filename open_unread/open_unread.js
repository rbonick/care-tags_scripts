javascript: (
	function(){
		var elements = document.getElementsByTagName("a");
		for (var i=0; i<elements.length; ++i){
			var currelem = elements[i];
			if(currelem.href.indexOf("unread") != -1){
				window.open(currelem.href, "_blank");
			}
		}
	}
)
();