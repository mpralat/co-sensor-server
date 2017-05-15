document.addEventListener("DOMContentLoaded", function() {
  main();
});

var chart = null;
var socket = null;

function main() {
    chart = createChart();

    socket = createSocket();
}

function createChart() {
    var canvas = document.getElementById('chart');

    var datasets = [{
        label: 'CO ppm',
        data: [],
        strokeColor: "rgba(51, 195, 240, 0.9)",
        fillColor: "rgba(51, 195, 240, 0.9)"
    }];

    var data = {
        datasets: datasets
    };

    var options = {
        responsive: true,
        scales: {
            xAxes: [{
                type: "time",
                display: true,
                scaleLabel: {
                    display: true,
                    labelString: 'Date'
                }
            }],
            yAxes: [{
                display: true,
                scaleLabel: {
                    display: true,
                    labelString: 'value'
                }
            }]
        }
    };

    return Chart.Line(canvas,{
        type: 'line',
        data: data,
        options: options
    });
}

function addValue(chart, timestamp, value){
    var data = chart.data.datasets[0].data;

    if (data.length > 20) {
        data.shift();
    }

    data.push({
        'x': timestamp,
        'y': value
    });
    chart.update();
}

function createSocket() {
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
        addValue(chart, timestamp, value);
    });
}