var basic_color = "#B0B0B0";
var today_color = "#696969";
var weekdays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
var daytimes = ['Morning', 'Midday', 'Evening', 'Night'];
var daytimes_colors = {"dangerous": "#ff2f2f", "medium": "#ffe12f","normal": "#ccff66", "healthy": "#4dff4d" };

function createAvgChart(colors, labels, data_to_insert, title, canvas) {
    var datasets = [{
        data: data_to_insert,
        backgroundColor: colors
    }];

    var data = {
        labels: labels,
        datasets: datasets
    };

    var options = {
       legend: { display: false },
        title: {
            display: true,
            text: title
      }
    };

    return Chart.Bar(canvas,{
        type: 'bar',
        data: data,
        options: options
    });
}

function addAvgValue(timestamp, value){
    weekday_index = getWeekDayNumber(timestamp);
    daytime_index = getDaytime(timestamp);
    updateChart(avg_chart, weekday_index, value, averages, counts);
    updateChart(week_avg_chart, daytime_index, value, daytime_avgs, daytime_counts);
}

function updateChart(chart, index, value, avgs, counts) {
    console.log(avgs[index]);
    counts[index] += 1;
    avgs[index] = (avgs[index] * counts[index] + value) / counts[index];
    chart.data.datasets[0].data = avgs;
    chart.update();
}

// MONTH AVG
function getWeekDayNumber(timestamp) {
    var d = new Date(Date.parse(timestamp + "Z"));
    return d.getDay();
}
function createMonthAvgChart() {
    var canvas = document.getElementById('chart');
    var colors = prepareColours();
    return createAvgChart(colors, weekdays, averages, 'Average CO values from last month', canvas);
}

// WEEK AVG
function getDaytime(timestamp) {
    var d = new Date(Date.parse(timestamp + "Z"));
    var hour = d.getHours();
    if (hour > 6 && hour <= 12)
        return 0;
    else if (hour > 12 && hour <= 18)
        return 1;
    else if (hour > 18 && hour <= 24)
        return 2;
    return 3;
}

function prepareColours() {
    var d = new Date();
    var dayOfWeek = d.getDay();
    var backgrounds = Array(7).fill(basic_color);
    backgrounds[dayOfWeek] = today_color;
    return backgrounds;
}

function prepareDaytimeColours(data) {
    var labels = [];
    for (var i=0; i < data.length; i++) {
        labels.push(daytimes_colors[getStyle(data[i])]);
    }
    return labels;
}

function createWeekAvgChart() {
    var canvas = document.getElementById('week_chart');
    var data = daytime_avgs;
    var colors = prepareDaytimeColours(daytime_avgs);
    return createAvgChart(colors, daytimes, data, "Average CO values from last week", canvas);
}