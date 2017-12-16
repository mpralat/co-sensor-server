document.addEventListener("DOMContentLoaded", function() {
  main();
});

var avg_chart = null;
var week_avg_chart = null;
var sockets = [];
var critical_value = 5.0;

function main() {
    avg_chart = createMonthAvgChart();
    week_avg_chart = createWeekAvgChart();
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

    for (var i = 0; i < sensors_nums.length; i++) {
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
    this.consumeMessage(data, serial_num);
}

function consumeData(data, serial_num) {
    var frames = data;
    if (!(frames instanceof Array)) {
        frames = [frames];
    }
    frames.forEach(function(frame){
        var value = parseFloat(frame['value']);
        var timestamp = new Date(Date.parse(frame['timestamp']));
        addAvgValue(timestamp, value);
        refreshCurrentValue(value, serial_num);
    });
}

function roundUp(num, precision) {
  precision = Math.pow(10, precision);
  return Math.ceil(num * precision) / precision
}

function getStyle(value) {
    if (value < 5)
        return "healthy";
    else if (value < 9)
        return "normal";
    else if (value < 24)
        return "medium";
    return "dangerous";
}

function refreshCurrentValue(value, serial_num) {
    var div = document.getElementById(serial_num);
    div.innerHTML = sensors_data[serial_num] + ": " + roundUp(value, 2);
    div.className = getStyle(value) + " box";
}