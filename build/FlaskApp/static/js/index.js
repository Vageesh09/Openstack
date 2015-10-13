

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
}



function displayStatus(){

	var result = sendRequest('/status','GET');
	var statOBJ = getJsonObj(result);
	console.log(statOBJ)
	if(statOBJ.error == 'GOOD'){
		error=0
		active=0;
		for(i=0;i<statOBJ.count;i++){
			if(statOBJ.status == "ACTIVE")
				active++;
			else if(statOBJ.status == "ERROR")
				error++
		}

		var l1 = document.createElement("label");
  		l1.innerHTML = "Total";
  		var l2 = document.createElement("label");
  		l2.innerHTML = statOBJ.count; 
  		var l3 = document.createElement("label");
  		l3.innerHTML = "Active"; 
  		var l4 = document.createElement("label");
  		l4.innerHTML = active; 
  		var l5 = document.createElement("label");
  		l5.innerHTML = "Error";
  		var l6 = document.createElement("label");
  		l6.innerHTML = error;

  		$("#statusVmLeft").append(l1,l2,l3,l4,l5,l6);



	}

}