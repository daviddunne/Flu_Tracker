/**
 * Created by david on 28/03/16.
 */

//http://stackoverflow.com/questions/10082330/dynamically-create-bootstrap-alerts-box-through-javascript
function create_bootstrap_alert(message) {
    $('#alert').html($('#alert').html() +
        '<div class="alert alert-danger" style="margin-top:0px; margin-bottom:0px;">' +
        '<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>' +
        '<span><strong>' + 'Alert: ' + '</strong>' + message + '</span></div>');
}