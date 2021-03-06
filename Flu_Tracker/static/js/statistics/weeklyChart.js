//  Author: David Dunne,    Student Number: C00173649,    Date Created: 28th Jan 2016

var data;
var option;
//========================================================================================
//Re-draw chart when window size changes
//========================================================================================
$(window).on('resize', function(){
    var width = $('#text_display').width();
    $('#weekly_chart').css({"width":width, "height":"auto"});
    var ctx = document.getElementById("weekly_chart").getContext('2d');
    var weekly_line_chart = new Chart(ctx).Line(data, option);
});

//========================================================================================
// Draw weekly count line chart when doc loads
//========================================================================================
$(document).ready(function (){
    var returnedData;
    var labels = [];
    var values = [];
     $.ajax({
        url: '/get/weekly/chart/data',
        type: 'GET',
        dataType: "json",
        success: function (response) {
            var responseValue = response['results'];
            returnedData = responseValue['data'];

            for(var key in returnedData) {
                if(returnedData.hasOwnProperty(key)) {
                    labels.push("week " + key);
                    values.push(returnedData[key]);
                }
            }

            $(function() {
                data = {
                labels: labels, //labels for x axis
                datasets: [
                    {
                        label: "2016",
                        fillColor: "#FCAC45",
                        strokeColor: "rgb(211, 84, 0)",
                        pointColor: "rgba(153,0,76,0.2)",
                        pointStrokeColor: "#fff",
                        pointHighlightFill: "#fff",
                        pointHighlightStroke: "rgba(153,0,76,0.2)",
                        data: values
                    },
                ]
            };
            option = {
                datasetFill: false,
            };
            var ctx = document.getElementById("weekly_chart").getContext('2d');
            var weekly_line_chart = new Chart(ctx).Line(data, option);
            });
        },
        error: function () {
            create_bootstrap_alert('Error while loading weekly count graph');
        }
    });
});


