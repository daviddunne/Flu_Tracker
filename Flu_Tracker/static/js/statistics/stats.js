/**
 * Created by david on 27/01/16.
 */
// Scripts to display statistics/counts
$(document).ready(function(){

    var date = getDayMonthYear();
    setStatsCounts(date.day, date.month, date.year)
});


// Set count values for statistics
function setStatsCounts(day, month, year){
     $.ajax({
        url: '/get/stats/count',
        type: 'GET',
        data: {day : day, month: month, year: year},
        dataType: "json",
        success: function (response) {
            var responseValue = response['results'];
            var today_count = responseValue['today'];
            var month_count = responseValue['month'];
            var year_count = responseValue['year'];
            var all_count = responseValue['all'];
            $('#today').html(today_count);
            $('#this_month').html(month_count);
            $('#this_year').html(year_count);
            $('#all_time').html(all_count);
        },
        error: function () {
            $('#today').html('Error');
            $('#this_month').html('Error');
            $('#this_year').html('Error');
            $('#all_time').html('Error');
            create_bootstrap_alert('Error while retrieving counts for statistics');
        }
    });
};

function getDayMonthYear() {
    // get date and standardise it
    var d = new Date();
    var day = d.getDate();
    var month = d.getMonth() + 1;
    var year = d.getFullYear();
    if (day < 10) {
        day = '0' + day;
    }
    if (month < 10) {
        month = '0' + month
    }
    ;
    return {day: day, month: month, year: year};
}