/**
 * Created by david on 01/01/16.
 */
//  Script used when categorising tweets for training purposes
$(function() {
    var $id = $('#tweetId');

    $.ajax({
        url: '/getuncategorisedtweet',
        type: 'GET',
        dataType: "json",
        success: function (response) {
            var responseValue = response['results'];
            var text = responseValue['text'];
            var id = responseValue['id'];
            document.getElementById('sentence').innerHTML = text;
            document.getElementById('tweetId').value = id;
            if(text === "NO TWEET AVAILABLE, PLEASE REFRESH"){
                document.getElementById("submitButton").disabled = true;
            }
        },
        error: function () {
            alert('Error when getting tweet from database');
        }
    });

    $("#submitButton").on('click',function(e){
        // Needed to stop jquery firing twice
        e.preventDefault();
        e.stopImmediatePropagation();
        document.getElementById('submitButton').disabled = true;
        document.getElementById('submitButton').value = "Submitting..."
        var data = {
            id: $('#tweetId').val(),
            text:$('#sentence').text(),
            sentiment: $('input:radio[name=flu]:checked').val()
        };
        $.ajax({
            url: '/update/tweet/sentiment',
            type: 'PUT',
            data: data,
            success: function(response) {
                var responseValue = response['results'];
                var updatedTweets = responseValue['count'];
                if (updatedTweets == 1){
                    window.location.reload(true);
                }
                else {
                    alert("Error: failed to update record");
                }
            }
        });
    });
});