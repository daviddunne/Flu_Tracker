/**
 * Created by david on 28/01/16.
 */


$(document).ready(function (){
     $.ajax({
        url: '/get/weekly/chart/data',
        type: 'GET',
        dataType: "json",
        success: function (response) {

            var responseValue = response['results'];
            var returnedData = responseValue['data'];
            var labels = [];
            var values = [];

            for(var key in returnedData) {
                if(returnedData.hasOwnProperty(key)) {
                    labels.push("week " + key);
                    values.push(returnedData[key]);
                }
            }

            $(function() {
                var data = {
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
            var option = {
                datasetFill: false,
            };
            var ctx = document.getElementById("weekly_chart").getContext('2d');
            var weekly_line_chart = new Chart(ctx).Line(data, option);
            });
        },
        error: function () {
            alert("Error while getting weekly graph data")
        }
    });
});

