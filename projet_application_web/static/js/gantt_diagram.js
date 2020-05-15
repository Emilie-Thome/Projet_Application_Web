const name = JSON.parse(document.getElementById('name').textContent);
const infos_gantt = JSON.parse(document.getElementById('infos-gantt').textContent);

// Chart options initialized
const gantt_options = {
    title: {
        text: 'Gantt Diagram'
    },
    series: [{
        name: name,
        data: []
    }]
};

// Chart options filled
for (var info of infos_gantt) {
    let start = info["start"];
    let end = info["end"];
    gantt_options.series[0].data.push({
        name: info["name"],
        start: Date.UTC(start[0], start[1]-1, start[2]),
        end: Date.UTC(end[0], end[1]-1, end[2]),
    })
}

Highcharts.ganttChart('gantt', gantt_options);