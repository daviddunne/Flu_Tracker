// Define global variables.
var map, heatmap, userDefinedLocation;
var defaultLocation = new google.maps.LatLng(53.574543437408934, -15.490722653750026);// Default location of Mid Atlantic Ocean for now
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
            alert("Location not found.");
            document.getElementById('searchmap').focus();
        }
    });
}

// updating map overlay
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

// Function to call moveToLocation with point when enter pressed on location input box.
function keyPress(e){
    var x = e || window.event;
    var key = (x.keyCode || x.which);
    if(key == 13 || key == 3){
        var location = document.getElementById('searchmap').value;
        moveToLocation(location);
    }
}

// display texts of tweets
function displayTweet_Texts(lat, lng) {
    var time_filter_label_text = $('#time_filter_label').text();

    //get the date elements from text of label
    time_filter_label_text = time_filter_label_text.split(' ');
    var start_date = time_filter_label_text[2];
    var end_date = time_filter_label_text[4];
    // activate loading gif
    $body = $("body");
    $body.addClass("loading");
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

        }
    });
    // creates table for tweet texts
    function constructHTMLTableForTweets(points) {
        console.log(points);
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
                    "<tr><th colspan='4 id='table-heading'><h4>Geo-Relevant Data</h4></br></th></tr>" +
                    "<tr><th colspan='3'><strong>Instance Count</strong></th><td>" + row_count + "</td></tr>"
                    "<tr><td colspan='3'><strong>50km Radius around point <br/>Latitude:  </strong>" + lat + "<strong><br/>Longitude:  </strong>" + lng + "</td>" +
                    "<td>Please note no filter applied to text. User discretion is advised.</td></tr>" +
                    "<tr><th>Date</th><th>Latitude</th><th>Longitude</th><th>Text</th></tr>";

        html = html + table_rows_html;
        html = html + "</table><button type='button' class='mapBtn' onclick='clearText()'>Clear All</button><input"

        return html
    }
}
// Clear tweet text
function clearText() {
    $('#text_display').fadeOut('slow');
    window.location.href ="#tf-meetFluTrakR"
}




