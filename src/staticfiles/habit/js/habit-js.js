


"use strict";


function addChild() {
	//alert( 'Javascript click is doing stuff!!!!' );
	document.getElementById('reply-to-comment').style.display = 'block';
	//alert( 'Javascript click is doing stuff!!!!' );
}

function greet() {
    document.getElementById('result').innerHTML = 'Hello World';
    return false;
}

document.getElementById('go').addEventListener('click', greet);