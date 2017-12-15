
// https://developers.google.com/maps/documentation/javascript/markers
// https://www.patrick-wied.at/static/heatmapjs/
// https://www.patrick-wied.at/static/heatmapjs/example-heatmap-googlemaps.html

document.addEventListener("DOMContentLoaded", function() {
    main();
});

var map = "";

function main() {
    initMap();
}

function initMap() {
    var default_center = {lat: 52.409538, lng: 16.931992};
    var mapOptions = {
        zoom: 12,
        center: default_center
    };
    map = new google.maps.Map(document.getElementById("map"), mapOptions);

    setMarkerOnMap(52.409538, 16.931992, "marker_test");
}

function setMarkerOnMap(lat, lng, title) {
    var marker_position = {lat: lat, lng: lng};
    var marker = new google.maps.Marker({
        position: marker_position,
        title: title,
        animation: google.maps.Animation.DROP,
        map: map
    });
    marker.addListener('click', function ()  {
        toggleBounce(marker);
    }, false);

    // To add the marker to the map, call setMap(); (if no map set in marker)
    // marker.setMap(map);

    // remove marker:
    // marker.setMap(null);
}

function toggleBounce(marker) {
    if (marker.getAnimation() !== null) {
        marker.setAnimation(null);
    } else {
        marker.setAnimation(google.maps.Animation.BOUNCE);
    }
}
