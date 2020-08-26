


"use strict";


function addChild(pk) {
	//
	if(document.getElementById(pk).style.display == 'none'){
		alert( 'show reply box' + pk );
		document.getElementById(pk).style.display = 'block';
	}else{
		alert( 'hide reply box' + pk );
		document.getElementById(pk).style.display = 'none';
	}
	//alert( 'Javascript click is doing stuff!!!!' );
}

function greet() {
    document.getElementById('result').innerHTML = 'Hello World';
    return false;
}

document.getElementById('go').addEventListener('click', greet);