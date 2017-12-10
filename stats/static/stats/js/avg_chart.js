function createAvgChart() {
    var canvas = document.getElementById('chart');
    var datasets = [{
        data: averages,
        backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850"]
    }];

    var data = {
        labels: ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
        datasets: datasets
    };

    var options = {
       legend: { display: false },
        title: {
            display: true,
            text: 'Average CO values from last month'
      }
    };

    return Chart.Bar(canvas,{
        type: 'bar',
        data: data,
        options: options
    });
}

function getWeekDayNumber(timestamp) {
    var d = new Date(Date.parse(timestamp + "Z"));
    return d.getDay();
}

function addAvgValue(chart, timestamp, value){
    console.log('AVG UPDATE!! ');
    index = getWeekDayNumber(timestamp);
    console.log(index);
    counts[index] += 1;
    console.log(counts);
    averages[index] = (averages[index] * counts[index] + value) / counts[index];
    console.log(averages);
    chart.data.datasets[0].data = averages;
    chart.update();
}