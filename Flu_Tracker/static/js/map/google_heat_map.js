//  Author: David Dunne,    Student Number: C00173649, Created Jan 2016

// Define global variables.
var map, heatmap, userDefinedLocation;
// Default location of Mid Atlantic Ocean
var defaultLocation = new google.maps.LatLng(53.574543437408934, -15.490722653750026);
var zoomValue = 4;
var mapdatapoints = [];


//========================================================================================
// Initilise map.
//========================================================================================
function initMap () {

    // Enabling new cartography and themes.
    var mapContainer;
    var mapOptions;
    google.maps.visualRefresh = true;
    // Initialise time filter settings
    document.getElementById("time_filter_label").innerHTML = "Slide left/right to view data for previous 30 days";

    // Set starting options of map , location, zoom level, type of map, UI and scroll wheel options.
    mapOptions = {
        center: defaultLocation,
        zoom: zoomValue,
        mapTypeId: google.maps.MapTypeId.HYBRID,
        scrollwheel: false,
        zoomControl: true,
        panControl:false,
        streetViewControl: false,
        position:google.maps.ControlPosition.TOP_RIGHT
    };

    // Getting map DOM element.
    mapContainer = document.getElementById('map_container');

    // Creating a map with DOM element which is just obtained
    map = new google.maps.Map(mapContainer, mapOptions);
    // add event listener for map to get location on click and display texts
    google.maps.event.addListener(map, 'click', function(e) {
        displayTweet_Texts(e.latLng.lat(), e.latLng.lng());
       });
    // set selected index of slide-bar
    document.getElementById('time_filter').selectedIndex ="0";
    //Creating the heat-map layer
    heatmap = new google.maps.visualization.HeatmapLayer({
        data: mapdatapoints
    });
    // Adding heat-map layer to the map.
    heatmap.setMap(map);
}


//========================================================================================
// Repositions the map to location entered by user.
//========================================================================================
function moveToLocation(){
    // Get location from location filter
    var location = document.getElementById('searchmap').value;
    // Find geolocation for location entered by user
    var geocoder =  new google.maps.Geocoder();
    geocoder.geocode( { 'address': location}, function(results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            var geolocation = results[0].geometry.location;
            var lat = geolocation.lat();
            var long = geolocation.lng();
            // Set userDefinedLocation variable
            userDefinedLocation = new google.maps.LatLng(lat, long);
            // Center the map on that location
            map.setCenter(userDefinedLocation);
            // Set appropriate zoom level for specified location
            map.fitBounds(results[0].geometry.viewport);
            // Reset search input box to empty
            document.getElementById('searchmap').value = '';
            // Set zoomValue variable to current zoom level
            zoomValue = map.getZoom();
          }
        else {
            // No result for filtered location.
            create_bootstrap_alert("Location not found.");
            document.getElementById('searchmap').focus();
        }
    });
}

//========================================================================================
// Function to update map overlay
//========================================================================================
function updateHeatMap(){
    // Clear any existing overlay.
    heatmap.setMap(null);
    // Create new overlay based on appropriate values for selection.
    heatmap = new google.maps.visualization.HeatmapLayer({
        data: mapdatapoints

    });
    // Set the overlay.
    heatmap.setMap(map);
}
// Pick up a Key Press for enter in location filter.
document.onkeypress = keyPress;


//========================================================================================
// Function to call moveToLocation with point when enter pressed on location input box.
//========================================================================================
function keyPress(e){
    var x = e || window.event;
    var key = (x.keyCode || x.which);
    if(key == 13 || key == 3){
        var location = document.getElementById('searchmap').value;
        moveToLocation(location);
    }
}

//========================================================================================
// Function to display texts of tweets
//========================================================================================
function displayTweet_Texts(lat, lng) {
    // activate loading gif
    $body = $("body");
    $body.addClass("loading");
    //get the date elements from text of label
    var time_filter_label_text = $('#time_filter_label').text();
    time_filter_label_text = time_filter_label_text.split(' ');
    var start_date = time_filter_label_text[2];
    var end_date = time_filter_label_text[4];

    // send ajax call to endpoint
    $.ajax({
        url: '/get/data/points/for/area',
        type: 'GET',
        data: {
            lat : lat,
            lng: lng,
            start_date: start_date, end_date: end_date
        },
        dataType: "json",
        success: function(response) {
            var display = $('#text_display');
            var responseValue = response['data'];
            var html = constructHTMLTableForTweets(responseValue);
            $body.removeClass("loading");
            display.html(html);
            display.fadeIn('slow');

        },
        error: function () {
            $body.removeClass("loading");
            create_bootstrap_alert('Error while retrieving text for location <strong>lat: </strong>' + lat +
                                    '<strong> long: </strong>' + lng + ' between ' + start_date + ' and ' + end_date);
        }
    });
    // creates table for tweet texts
    function constructHTMLTableForTweets(points) {
        var table_rows_html = "";
        var row_count = 0;
        for(var i = 0; i < points.length; i++) {
            table_rows_html = table_rows_html +
                "<tr>" +
                    "<td>" + points[i]['date'] + "</td>" +
                    "<td>" + points[i]['lat'] + "</td>" +
                    "<td>" + points[i]['long'] + "</td>" +
                    "<td>" + points[i]['text'] + "</td>" +
                "</tr>";
            row_count = row_count + 1;
        }

        var html =
                "<table class='table' id='map_click_data'>" +
                    "<tr><th colspan='4' id='table-heading' >Geo-Relevant Data</br></th></tr>" +
                    "<tr><th colspan='4' style='font-weight:500; font-size:20px;'>Instance Count: "+ row_count + " </th></tr>" +
                    "<tr><td colspan='4'><span style='font-weight:500; font-size:20px;'>Click Location: </span>" +
                    "<i style='color:#FCAC45;'>Latitude: </i>" + lat + " <i style='color:#FCAC45;'>Longitude: </i>" + lng + "</td></tr>" +
                    "<tr><td colspan='4' style='color:#FCAC45;'>Please note no filter applied to text. User discretion is advised.</td></tr>" +
                    "<tr style='font-weight:500; font-size:20px;'><th>Date</th><th>Latitude</th><th>Longitude</th><th>Text</th></tr>";

        html = html + table_rows_html;
        html = html + "</table><button type='button' class='mapBtn' onclick='hideTweetText()'>Clear All</button><input"

        return html
    }
}
//========================================================================================
// HIDE TWEET TEXT DIV
//========================================================================================
function hideTweetText() {
    $('#text_display').fadeOut('slow');
    window.location.href ="#tf-meetFluTrakR"
}

//========================================================================================
// UPDATE MAP WHEN PAGE LOADS
//========================================================================================
$(document).ready(function() {
    $('#time_filter').on('change', updateMapOnSliderChange);
});

$(document).ready(function(){
    document.getElementById("time_filter").value = 1;
    updateMapOnSliderChange();
});

//========================================================================================
// UPDATE MAP FUNCTION WHEN SLIDER BAR IS CHANGED BY THE USER
//========================================================================================
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
        },
        error: function () {
            $body.removeClass("loading");
            create_bootstrap_alert('Error while updating map');
        }
    });
}
