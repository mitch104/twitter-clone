$(document).ready(function() {
    // Like/Unlike functionality
    $('.like-btn').click(function() {
        const tweetId = $(this).data('tweet-id');
        const likeBtn = $(this);
        const likeCount = likeBtn.find('.like-count');
        
        $.ajax({
            url: `/tweet/${tweetId}/like/`,
            method: 'GET',
            success: function(data) {
                if (data.liked) {
                    likeBtn.addClass('active');
                    likeBtn.find('i').removeClass('far').addClass('fas');
                } else {
                    likeBtn.removeClass('active');
                    likeBtn.find('i').removeClass('fas').addClass('far');
                }
                likeCount.text(data.likes_count);
            }
        });
    });
    
    // Retweet functionality
    $('.retweet-btn').click(function() {
        const tweetId = $(this).data('tweet-id');
        const retweetBtn = $(this);
        const retweetCount = retweetBtn.find('.retweet-count');
        
        $.ajax({
            url: `/tweet/${tweetId}/retweet/`,
            method: 'GET',
            success: function(data) {
                if (data.retweeted) {
                    retweetBtn.addClass('active');
                } else {
                    retweetBtn.removeClass('active');
                }
                retweetCount.text(data.retweets_count);
                
                // Refresh the timeline to show the new retweet
                if (data.retweeted) {
                    setTimeout(function() {
                        location.reload();
                    }, 1000);
                }
            }
        });
    });
    
    // Share functionality
    $('.share-btn').click(function() {
        const tweetId = $(this).data('tweet-id');
        const url = window.location.origin + `/tweet/${tweetId}/`;
        
        // Create a temporary input element
        const tempInput = document.createElement('input');
        tempInput.value = url;
        document.body.appendChild(tempInput);
        
        // Select and copy the URL
        tempInput.select();
        document.execCommand('copy');
        document.body.removeChild(tempInput);
        
        // Show a tooltip or alert
        alert('Link copied to clipboard: ' + url);
    });
}); 