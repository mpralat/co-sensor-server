document.addEventListener("DOMContentLoaded", function() {
  main();
});

var chart = null;

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

function main() {
    chart = createChart();

    createSocket();
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
    socket.onmessage = consumeMessage;
}

function consumeMessage(message) {
    console.log(message.data);
    var data = JSON.parse(message.data);
    console.log(data);
    var frame = data['text'];
    var value = parseFloat(frame['value']);
    var timestamp = new Date(Date.parse(frame['timestamp']));
    console.log(timestamp);
    console.log(value);
    addValue(chart, timestamp, value);
}