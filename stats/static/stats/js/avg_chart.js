var basic_color = "#B0B0B0";
var today_color = "#696969";
var weekdays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
var daytimes = ['Morning', 'Midday', 'Evening', 'Night'];
var daytimes_colors = {"dangerous": "#ff2f2f", "medium": "#ffe12f","normal": "#ccff66", "healthy": "#4dff4d" };

w_avg = averages;
d_avg = daytime_avgs;
w_counts = counts;
d_counts = daytime_counts;

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
    // update avg chart
    w_avg[weekday_index] = (w_avg[weekday_index] * w_counts[weekday_index] + value) / (w_counts[weekday_index] + 1);
    w_counts[weekday_index] += 1;
    avg_chart.data.datasets[0].data = w_avg;
    avg_chart.update();
    // update week chart
    d_avg[daytime_index] = (d_avg[daytime_index] * d_counts[daytime_index] + value) / (d_counts[daytime_index] + 1);
    d_counts[daytime_index] += 1;
    week_avg_chart.data.datasets[0].data = d_avg;
    week_avg_chart.update();
}

function updateChart(chart, index, value, avgs, counts) {
    console.log(avgs[index]);

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