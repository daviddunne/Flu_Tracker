/**
 * Created by david on 20/04/16.
 */
function checkForm(){
    var inEmail = $('#inputEmail');
    var inMsg = $('#inputMessage');

    if((inEmail[0].checkValidity() == false) && (inMsg[0].checkValidity() == false)){
        inEmail.css("border-color","red");
        inMsg.css("border-color","red");
    }
    else if((inEmail[0].checkValidity() == false) && (inMsg[0].checkValidity() == true)){
        inEmail.css("border-color","red");
        inMsg.css("border-color","#fff");
    }
    else if((inEmail[0].checkValidity() == true) && (inMsg[0].checkValidity() == false)){
        inEmail.css("border-color","#fff");
        inMsg.css("border-color","red");
    }
    else {
        inEmail.css("border-color","#fff");
        inMsg.css("border-color","#fff");
        sendEmail();

    }
}

function sendEmail() {
    window.location.href ="#tf-contact";
    var button = $('#submitMsgBtn');
    var emailInput =  $('#inputEmail');
    var msgInput =  $('#inputMessage');
    var status = $('#messageStatus');

    button.attr("disabled", true);
    var subject = "Message from Flu-TrakR User";
    var email = emailInput.val();
    var message = msgInput.val();

    $.ajax({
        url: '/send/email',
        type: 'POST',
        data: {email: email, subject:subject, message:message},
        dataType: "json",
        success: function (response) {
            status.text("Message Sent!");
            status.css({"display":"block","color":"white"});
            emailInput.val("");
            msgInput.val("");
            button.attr("disabled", false);
        },
        error: function () {
            status.text("Message Failed!");
            status.css({"display":"block","color":"red"});
            button.attr("disabled", false);
        }
    });
}