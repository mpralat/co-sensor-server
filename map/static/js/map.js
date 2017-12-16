const minCoValue = 4.5;
const maxCoValue = 5.7;

// -------------------------

document.addEventListener("DOMContentLoaded", function() {
    main();
});

var default_center = {lat: 52.409538, lng: 16.931992};
var myOptions = {
    zoom: 12,
    center: default_center
};

var map = null;
var heatmap = null;
var sockets = [];

function main() {
    prepareHeatMap();
    sockets = createSockets('map');
}

function prepareHeatMap() {
    map = new google.maps.Map(document.getElementById("map"), myOptions);
    heatmap = new HeatmapOverlay(map,
        {
        "radius": 0.005,
        "maxOpacity": 0.5,
        "scaleRadius": true,
        "useLocalExtrema": false,
        latField: 'lat',
        lngField: 'lng',
        valueField: 'co_value'
        }
    );
    for (var i = 0; i < sensors_list.length; i++) {
        setMarkerOnMap(sensors_list[i]);
    }
}

function setMarkerOnMap(sensor) {
    var marker_position = {lat: sensor.lat, lng: sensor.lng};
    var marker = new google.maps.Marker({
        position: marker_position,
        title: sensor.name,
        map: map
    });
    marker.addListener('click', function ()  {
        displayMarkerInfo(sensor);
    }, false);
}

function displayMarkerInfo(sensor) {
    var markerInfoField = document.getElementById("markerInfo");
    markerInfoField.innerHTML = sensor.name + " (" + sensor.serial_number + ")";
}

function createSockets(sufix) {
    var protocol;
    if (window.location.protocol === 'https:'){
        protocol = 'wss:';
    } else {
        protocol = 'ws:'
    }

    var port = '';
    if (window.location.port !== ''){
        port = ':' + window.location.port;
    }

    for (var i = 0; i < sensors_list.length; i++) {
        var sensor = sensors_list[i];
        console.log("Sensor's serial_no: " + sensor.serial_number);
        var socket = createSingleSocket(sensor.serial_number, protocol, port, sufix);
        socket.consumeMessage = consumeData;
        socket.onmessage = parseMessage;
        sockets.push(socket);
    }
    return sockets;
}

function createSingleSocket(serialNumber, protocol, port, sufix) {
    var url = protocol + '//' + window.location.hostname + port;
    url += '/sensors/room/' + serialNumber + '/' + sufix;

    return new WebSocket(url);
}

function parseMessage(message) {
    var data = JSON.parse(message.data);
    var parsed_url = message.target.url.split('/');
    var serial_num = parsed_url[parsed_url.length - 2];
    this.consumeMessage(data, serial_num);
}

function consumeData(data, serial_num) {
    var frames = data;
    if (!(frames instanceof Array)) {
        frames = [frames];
    }
    frames.forEach(function(frame){
        var value = parseFloat(frame['value']);
        var timestamp = "";
        if (frame['timestamp'] !== "")
            timestamp = new Date(Date.parse(frame['timestamp']));
        updateSensorValue(serial_num, value, timestamp);
        updateMap();
    });
}

function updateSensorValue(serial_num, value, timestamp) {
    for(var i = 0; i < sensors_list.length; i++) {
      if(sensors_list[i].serial_number === serial_num) {
        sensors_list[i].lastTimestamp = timestamp;
        sensors_list[i].co_value = value;
      }
    }
}

function updateMap() {
    console.log("UPDATE MAP: " + sensors_list.length);
    for(var i = 0; i < sensors_list.length; i++) {
        console.log(sensors_list[i].serial_number + " " + sensors_list[i].lat + " " + sensors_list[i].lng + " " + sensors_list[i].co_value)
    }
    var currentData = {
        max: maxCoValue,
        min: minCoValue,
        data: sensors_list
    };
    heatmap.setData(currentData);
}