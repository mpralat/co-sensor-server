document.addEventListener("DOMContentLoaded", function() {
  main();

});

var socket = null;

function main() {
    console.log(variable);
    socket = createSocket();
}

function createSockets() {
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

    var serialNumber = window.location.pathname.split('/')[3];

    var url = protocol + '//' + window.location.hostname + port;
    url += '/sensors/room/' + serialNumber + '/client';

    var socket = new WebSocket(url);

    socket.consumeMessage = consumeData;
    socket.onmessage = parseMessage;

    return socket;
}

function parseMessage(message) {
    var data = JSON.parse(message.data);
    socket.consumeMessage(data);
}

function consumeData(data) {
    var frames = data;
    if (!(frames instanceof Array)) {
        frames = [frames];
    }
    frames.forEach(function(frame){
        var value = parseFloat(frame['value']);
        var timestamp = new Date(Date.parse(frame['timestamp']));
        console.log(timestamp);
        console.log(value);
    });
}