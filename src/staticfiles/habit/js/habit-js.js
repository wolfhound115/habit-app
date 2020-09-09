


"use strict";
document.addEventListener('DOMContentLoaded', init, false);

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


$(function() {
   $('#go').on('click', greet);
});


$(document).ready( 
	function() {
		$("#about-btn").click( function(event) {
    		alert("You clicked the button using JQuery!");
	});


	$('#like-btn').click(function () {
            $.ajax({
                type: 'POST',

                url: $("#like-btn").attr("data-url"),
                data: {
                    'post_id': $("#like-btn").attr("data-post-id"),
                    'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                },
                success: LikePost,
                dataType: 'html'
            });

            function LikePost(data, jqXHR) {
                var data = $.parseJSON(data)
                if (data['liked']) {
                	document.getElementById('result').innerHTML = 'Click to like';
                    $('.thumb').removeClass("fas fa-thumbs-up").addClass('far fa-thumbs-up')
                } else {
                	document.getElementById('result').innerHTML = 'Click to unlike';
                    $('.thumb').removeClass("far fa-thumbs-up").addClass('fas fa-thumbs-up')
                }
            }
        });
});



function init(){
  function message () {
    alert("Hello!");
  }
  var button = document.getElementById('button');
  button.addEventListener('click', message, true);
}


/*
function LikePost(data, jqXHR) {
	alert("You clicked the button using JQuery!");
    var data = $.parseJSON(data)
    if (data['liked']) {
        $('#thumb').removeClass("fas fa-thumbs-up").addClass('far fa-thumbs-up')
    } else {
        $('#thumb').removeClass("far fa-thumbs-up").addClass('fas fa-thumbs-up')
    }
}
*/