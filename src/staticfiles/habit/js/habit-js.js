


"use strict";


function addChild(id) {
	//
	if(document.getElementById(id).style.display == 'none'){
		document.getElementById(id).style.display = 'block';
	}else{
		document.getElementById(id).style.display = 'none';
	}
}


$(function() {
	//doing it this way allows for it to work on newly loaded elements of infinite scroll too
	$('.container').on('click', '.post-like-btn', function () {
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
                	document.getElementById(data['post_like_button_text_id']).innerHTML = 'unlike';
                	document.getElementById(data['total_post_likes_id']).style.display = 'inline-block';
                	document.getElementById(data['total_post_likes_id']).innerHTML = data['new_total_post_likes'];
                } else {
                	document.getElementById(data['post_like_button_text_id']).innerHTML = 'like';
                	if(data['new_total_post_likes']){
                        document.getElementById(data['total_post_likes_id']).innerHTML = data['new_total_post_likes'];
	            	} else {
	            		document.getElementById(data['total_post_likes_id']).style.display = 'none';
	                	document.getElementById(data['total_post_likes_id']).innerHTML = data['new_total_post_likes'];
                	}
            	}
        }
    });



	//idk why but profile follow button started having CSRF token issues... Changing it from #profile-follow-btn to .profile-follow-btn for consistency in the meantime
	$('.profile-follow-btn').click(function () {
        $.ajax({
	        type: 'POST',
            url: $(this).attr("data-url"),
            data: {
                'profile_user_id': $(this).attr("data-profile-user-id"),
                //'total_post_likes': $("#total-post-likes").attr("data-total-post-likes"),
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
            },
            success: FollowProfile,
            dataType: 'html'
        });

        function FollowProfile(data, jqXHR) {
            var data = $.parseJSON(data)
            if (data['followed']) {
            	document.getElementById('profile-follow-btn').innerHTML = 'Followed';
            	document.getElementById("followers-count").innerHTML = data['new_total_followers'];
            } else {
                if (data['follow_back']) {
                    document.getElementById('profile-follow-btn').innerHTML = 'Follow Back';
                } else {
                    document.getElementById('profile-follow-btn').innerHTML = 'Follow';
                }
            	document.getElementById("followers-count").innerHTML = data['new_total_followers'];
            }
        }
    });

	$('.comment-like-btn').click(function () {
        $.ajax({
            type: 'POST',

            url: $(this).attr("data-url"),
            data: {
                'comment_id': $(this).attr("data-comment-id"),
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
            },
            success: LikeComment,
            dataType: 'html'
        });

        function LikeComment(data, jqXHR) {
            var data = $.parseJSON(data)
            if (data['liked']) {
            	document.getElementById(data['comment_like_button_text_id']).innerHTML = 'unlike';
            	document.getElementById(data['total_comment_likes_id']).style.display = 'inline-block';

            	document.getElementById(data['total_comment_likes_id']).innerHTML = data['new_total_comment_likes'];
            } else {
            	document.getElementById(data['comment_like_button_text_id']).innerHTML = 'like';
            	if(data['new_total_comment_likes'] > 0){
            		document.getElementById(data['total_comment_likes_id']).innerHTML = data['new_total_comment_likes'];	
            	} else {
            		document.getElementById(data['total_comment_likes_id']).style.display = 'none';
            		document.getElementById(data['total_comment_likes_id']).innerHTML = data['new_total_comment_likes'];
            	}
            	
            }
        }
    });
});

