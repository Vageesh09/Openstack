
function sendRequest(URL,METHOD) {
	response = "";

	if(URL == undefined || URL == ""){
		alert("empty url");
		return "empty_url";
	}

	var xhttp;
	if (window.XMLHttpRequest) {
	// code for modern browsers
		xhttp = new XMLHttpRequest();
	} else {
	// code for IE6, IE5
		xhttp = new ActiveXObject("Microsoft.XMLHTTP");
	}
	xhttp.onreadystatechange = function() {
		if (xhttp.readyState == 4 && xhttp.status == 200) {
			console.log(xhttp.responseText);
			response = xhttp.responseText;
			return response;
		}
	}
	xhttp.open(METHOD, URL, false);
	xhttp.send();
	return response;
	
}

