document.addEventListener("DOMContentLoaded", function(event) {
  main();
});

var myLineChart;

function addData(){
    myLineChart.data.datasets[0].data.shift();
    myLineChart.data.datasets[0].data.push(40 + Math.random() * 40);
    myLineChart.data.labels.shift();
    myLineChart.data.labels.push("Newly Added");
    myLineChart.update();
}

function main() {
    var canvas = document.getElementById('chart');

    var dataset = [];
    var x = 0;
    var y = 250;

    while (x < 180) {
        dataset.push({x: x, y: y});
        x += 1 + Math.random() * 0.2;
        y += Math.random() * 2 - 1;
    }

    var data = {
        datasets: [
            {
                label: "CO ppm",
                data: dataset
            }
        ]
    };

    console.log(data);

    var options = {
        type: 'linear',
        position: 'bottom'
    };

    console.log(options);

    myLineChart = Chart.Line(canvas,{
        type: 'line',
        data: {
            datasets: [{
                label: 'CO ppm',
                data: dataset,
                strokeColor: "rgba(51, 195, 240, 0.9)",
                fillColor: "rgba(51, 195, 240, 0.9)"
            }]
        },
        options: {
            scales: {
                xAxes: [{
                    type: 'linear',
                    position: 'bottom'
                }]
            }
        }
    });
}