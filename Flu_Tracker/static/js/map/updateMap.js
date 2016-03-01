// JQuery for Ajax call to database when time filter slidebar is changed
$(document).ready(function() {
    $('#time_filter').on('change', updateSlider);
});

function updateSlider() {
        var inputValue = $('#time_filter').val();
        $body = $("body");
        $body.addClass("loading");
        $('#text_display').fadeOut();
        $.ajax({
            url: '/getmappoints',
            type: 'POST',
            data: {time : inputValue},
            dataType: "json",
            success: function(response) {

                var responseValue = response['results'];
                var points = responseValue['datapoints'];
                var startdate = "" + responseValue['start_date'];
                var enddate = "" + responseValue['end_date'];

                // Set label for time slider
                document.getElementById("time_filter_label").innerHTML = "Date Range: " + startdate  + " - " + enddate;
               //Clear mapdatapoint
                mapdatapoints = [];

                // Get the number of entries in the data returned from ajax call
                var len = points.length;

                // Loop through data
                for(var i = 0; i < len; i++) {
                    var point = points[i];
                    // Extract latitude and longitude
                    var lat = point[0];
                    var long = point[1];
                    // Create map points with lat and long
                    var gPoint = new google.maps.LatLng(parseFloat(lat), parseFloat(long));
                    // Add points to mapdatapoints
                    mapdatapoints.push(gPoint);
                    $body.removeClass("loading");
                }
                updateHeatMap();

            }
        });
    }