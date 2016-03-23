// JQuery for Ajax call to database when time filter slide-bar is changed
$(document).ready(function() {
    $('#time_filter').on('change', updateMapOnSliderChange);
});

$(document).ready(function(){
    $('#time_filter').val(1);
    updateMapOnSliderChange();
});

function updateMapOnSliderChange() {
        var timeFromFilter = $('#time_filter').val();
        // Display loading gif
        $body = $("body");
        $body.addClass("loading");
        // Hide text from tweets if present
        $('#text_display').fadeOut();
        // Send Ajax call to API
        $.ajax({
            url: '/getmappoints',
            type: 'GET',
            data: {time : timeFromFilter},
            dataType: "json",
            success: function(response) {
                // Extract data from response
                var responseValue = response['results'];
                var points = responseValue['datapoints'];
                var startdate = "" + responseValue['start_date'];
                var enddate = "" + responseValue['end_date'];

                // Set label for time slider
                document.getElementById("time_filter_label").innerHTML = "Date Range: " + startdate  + " - " + enddate;
               // Clear mapdatapoint array
                mapdatapoints = [];

                // Get the number of entries in the data returned from ajax call
                var len = points.length;

                // Loop through data
                for(var i = 0; i < len; i++) {
                    // Select point from array
                    var point = points[i];
                    // Extract latitude and longitude from point
                    var lat = point[0];
                    var long = point[1];
                    // Create googlemap points with lat and long
                    var gPoint = new google.maps.LatLng(parseFloat(lat), parseFloat(long));
                    // Add googlemap point to mapdatapoints array
                    mapdatapoints.push(gPoint);
                }
                updateHeatMap();
                // Remove loading gif
                $body.removeClass("loading");
            }
        });
    }