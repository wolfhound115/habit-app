


"use strict";
document.addEventListener('DOMContentLoaded', init, false);

function addChild(id) {
	//
	if(document.getElementById(id).style.display == 'none'){
		alert( 'show reply box' + id );
		document.getElementById(id).style.display = 'block';
	}else{
		alert( 'hide reply box' + id );
		document.getElementById(id).style.display = 'none';
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

                url: $(this).attr("data-url"),
                data: {
                    'post_id': $(this).attr("data-post-id"),
                    //'total_post_likes': $("#total-post-likes").attr("data-total-post-likes"),
                    'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                },
                success: LikePost,
                dataType: 'html'
            });

            function LikePost(data, jqXHR) {
                var data = $.parseJSON(data)
                if (data['liked']) {
                	document.getElementById('like-btn-txt').innerHTML = 'unlike';
                	document.getElementById("total-post-likes").innerHTML = data['new_total_post_likes'];
                } else {
                	document.getElementById('like-btn-txt').innerHTML = 'like';
                	document.getElementById("total-post-likes").innerHTML = data['new_total_post_likes'];
                }
            }
        });


	$('.comment-like-btn').click(function () {
		alert($(this).attr('id'));
        $.ajax({
            type: 'POST',

            url: $(this).attr("data-url"),
            data: {
                'comment_id': $(this).attr("data-comment-id"),
                //'total_post_likes': $("#total-post-likes").attr("data-total-post-likes"),
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
            },
            success: LikeComment,
            dataType: 'html'
        });

        function LikeComment(data, jqXHR) {
            var data = $.parseJSON(data)
            if (data['liked']) {
            	alert("it has been liked")
            	document.getElementById(data['comment_like_button_text_id']).innerHTML = 'unlike';
            	document.getElementById(data['total_comment_likes_id']).style.display = 'inline-block';

            	document.getElementById(data['total_comment_likes_id']).innerHTML = data['new_total_comment_likes'] + " likes";
            } else {
            	document.getElementById(data['comment_like_button_text_id']).innerHTML = 'like';
            	if(data['new_total_comment_likes'] > 0){
            		alert("hi");
            		alert(document.getElementById(data['total_comment_likes_id']).style.display);
            		document.getElementById(data['total_comment_likes_id']).innerHTML = data['new_total_comment_likes']+ " likes";	
            	} else {
            		alert(data['total_comment_likes_id']);
            		document.getElementById(data['total_comment_likes_id']).style.display = 'none';
            		document.getElementById(data['total_comment_likes_id']).innerHTML = data['new_total_comment_likes'];
            	}
            	
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
