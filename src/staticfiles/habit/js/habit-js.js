


"use strict";
document.addEventListener('DOMContentLoaded', init, false);

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


	$('#post-like-btn').click(function () {
            $.ajax({
                type: 'POST',

                url: $("#post-like-btn").attr("data-url"),
                data: {
                    'post_id': $("#post-like-btn").attr("data-post-id"),
                    //'total_post_likes': $("#total-post-likes").attr("data-total-post-likes"),
                    'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                },
                success: LikePost,
                dataType: 'html'
            });

            function LikePost(data, jqXHR) {
                var data = $.parseJSON(data)
                if (data['liked']) {
                	document.getElementById('like-btn-txt').innerHTML = 'Like';
                	document.getElementById("total-post-likes").innerHTML = data['new_total_post_likes'];
                } else {
                	document.getElementById('like-btn-txt').innerHTML = 'Unlike';
                	document.getElementById("total-post-likes").innerHTML = data['new_total_post_likes'];
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
