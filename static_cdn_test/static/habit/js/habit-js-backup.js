


"use strict";
//document.addEventListener('DOMContentLoaded', init, false);

function addChild(pk) {
	//
	alert("something else");
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
    alert("Heres the greeting!");
    return false;
}

document.getElementById('go').addEventListener('click', greet);

$(document).ready( 
	alert("something something");
	function() {


    $("#about-btn").click( function(event) {
        alert("You clicked the button using JQuery!");
    });
});



function init(){
  function message () {
    alert("Hello!");
  }
  var button = document.getElementById('button');
  button.addEventListener('click', message, true);
};
function LikePost(data, jqXHR) {
	alert("You clicked the button using JQuery!");
    var data = $.parseJSON(data)
    if (data['liked']) {
        $('#thumb').removeClass("fas fa-thumbs-up").addClass('far fa-thumbs-up')
    } else {
        $('#thumb').removeClass("far fa-thumbs-up").addClass('fas fa-thumbs-up')
    }


}

