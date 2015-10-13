

function menuDropDown(){
	$("#menu_div").animate({
            width: 'toggle'

        });
}

function initializePage(){
	$('#statusVm_block').show();
	$('#createVm_block').hide();
	$('#deleteVm_block').hide();
	$('#console_block').hide();


	x=sendRequest('/test','GET');alert(x);

	var JSONObject = getJsonObj(x);
	alert(JSONObject.hello);
}