document.addEventListener("DOMContentLoaded", function() {
  main();
});

var avg_chart = null;
var sockets = [];

function main() {
    avg_chart = createAvgChart();
    sockets = createSockets();
}


function createSockets() {
    var protocol;
    var sufix = 'stats';
    if (window.location.protocol == 'https:'){
        protocol = 'wss:';
    } else {
        protocol = 'ws:'
    }

    var port = '';
    if (window.location.port != ''){
        port = ':' + window.location.port;
    }

    for (i = 0; i < sensors_nums.length; i++) {
        num = sensors_nums[i];
        socket = createSingleSocket(num, protocol, port, sufix);
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
    socket.consumeMessage(data, serial_num);
}

function consumeData(data, serial_num) {
    console.log(serial_num);
    var frames = data;
    if (!(frames instanceof Array)) {
        frames = [frames];
    }
    frames.forEach(function(frame){
        var value = parseFloat(frame['value']);
        var timestamp = new Date(Date.parse(frame['timestamp']));
        addAvgValue(avg_chart, timestamp, value);
        // refreshCurrentValue(value, serial_num);
    });
}

function refreshCurrentValue(value, serial_num) {
    console.log(value, serial_num)
}