const infos_activity = JSON.parse(document.getElementById('infos-activity').textContent);

// Chart options initialized
const activity_options = {
    chart: {
        type: 'column'
    },
    title: {
        text: 'Activity Diagram'
    },
    yAxis: {
        title:{
        text:'Entries in Histories'
        },
    },
    xAxis: {
        categories: [
            'Jan',
            'Feb',
            'Mar',
            'Apr',
            'May',
            'Jun',
            'Jul',
            'Aug',
            'Sep',
            'Oct',
            'Nov',
            'Dec'
        ],
        crosshair: true
    },
    plotOptions: {
        column: {
            pointPadding: 0.2,
            borderWidth: 0
        }
    },
    series: []
};
// Chart options filled
for (var info of infos_activity) {
    activity_options.series.push({
        name: info["member"],
        data: info["activity"],
    })
}

Highcharts.chart('activity', activity_options);