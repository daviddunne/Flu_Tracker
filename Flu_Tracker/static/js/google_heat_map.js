// Define global variables.
var map, heatmap, userDefinedLocation;
var defaultLocation = new google.maps.LatLng(53.574543437408934, -15.490722653750026);// Default location of Mid Atlantic Ocean for now
var zoomValue = 3;
var maxZoomValue = 2;

//========================================================================================
// Initilises map.
//========================================================================================
function initMap () {
    // Enabling new cartography and themes.
    var mapElement;
    var mapOptions;
    google.maps.visualRefresh = true;

    //Setting starting options of map , location, zoom level, type of map, UI and scroll wheel options.
    mapOptions = {
        center: defaultLocation,
        zoom: zoomValue,
        mapTypeId: google.maps.MapTypeId.ROADMAP,
        disableDefaultUI:true,
        scrollwheel: false
    };

    // Getting map DOM element.
    mapElement = document.getElementById('map_container');

    // Creating a map with DOM element which is just obtained
    map = new google.maps.Map(mapElement, mapOptions);
    document.getElementById('time_filter').selectedIndex ="0";
    //Creating the heatmap layer
    heatmap = new google.maps.visualization.HeatmapLayer({
        data: day
    });

    // Adding heatmap layer to the map.
    heatmap.setMap(map);

}
//========================================================================================
// Repositions the map to location entered by user.
//========================================================================================
function moveToLocation(location){
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

function updateHeatMap(timeperiod){
    // Clear any existing overlay.
    heatmap.setMap(null);
    // Create new overlay based on appropriate values for selection.
    if(timeperiod=='day'){
        heatmap = new google.maps.visualization.HeatmapLayer({
        data: day
        });
    }
    else if(timeperiod=='week') {
        heatmap = new google.maps.visualization.HeatmapLayer({
            data: week
        });
    }
    else if(timeperiod=='month') {
        heatmap = new google.maps.visualization.HeatmapLayer({
            data: month
        });
    }
    else if(timeperiod=='all') {
        heatmap = new google.maps.visualization.HeatmapLayer({
            data: all
        });
    }
    // Set the overlay.
    heatmap.setMap(map);
}

// Pick up a Key Press for enter in location filter.
document.onkeypress = keyPress;
// Function feeds location to zoomLocation.
function keyPress(e){
    var x = e || window.event;
    var key = (x.keyCode || x.which);
    if(key == 13 || key == 3){
        var location = document.getElementById('searchmap').value
        moveToLocation(location);
    }
}

// Zoom in or out depending on button pressed by user.
function zoomInOut(value){
    zoomValue = map.getZoom();
    zoomValue = zoomValue+value;
    if(zoomValue > maxZoomValue){
        map.setZoom(zoomValue);
    }
    else(alert("Max Zoom Level Reached"))

}

// Double Click Function on Map
function zoomInSmoothly(map, endZoom, startZoom) {


    if(endZoom < startZoom) {

        z = google.maps.event.addListener(map, 'zoom_changed', function (event) {
            google.maps.event.removeListener(z);
            zoomInSmoothly(map, endZoom, startZoom + 10);
        });
        setTimeout(function () {
            map.setZoom(startZoom)
            //ToDo this not working, need to reset the value of button
            (document.getElementById('zoomOut').value = '-');
        }, 500);
    }
}

