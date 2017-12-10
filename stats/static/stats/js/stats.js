document.addEventListener("DOMContentLoaded", function() {
  main();
});

var avg_chart = null;
var sockets = [];

function main() {
    avg_chart = createAvgChart();
    sockets = createSockets();
}

function createSockets(consumeData, parseMessage) {
    var protocol;
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
        socket = createSingleSocket(num, protocol, port);
        socket.consumeMessage = consumeData;
        socket.onmessage = parseMessage;
        sockets.push(socket);
    }
    return sockets;
}

function createSingleSocket(serialNumber, protocol, port) {
    var url = protocol + '//' + window.location.hostname + port;
    url += '/sensors/room/' + serialNumber + '/stats';

    console.log(url);
    return new WebSocket(url);
}

function parseMessage(message) {
    var data = JSON.parse(message.data);
    var serial_num = message.target.url.split('/');
    socket.consumeMessage(data, serial_num[serial_num.length - 2]);
}

function consumeData(data, serial_num) {
    var frames = data;
    if (!(frames instanceof Array)) {
        frames = [frames];
    }
    frames.forEach(function(frame){
        var value = parseFloat(frame['value']);
        var timestamp = new Date(Date.parse(frame['timestamp']));
        addAvgValue(avg_chart, timestamp, value);
        refreshCurrentValue(value, serial_num);
    });
}

function refreshCurrentValue(value, serial_num) {

}