const name = JSON.parse(document.getElementById('name').textContent);
const infos_gantt = JSON.parse(document.getElementById('infos-gantt').textContent);

// Chart options initialized
const options = {
    series: [{
        name: name,
        data: []
    }]
};

// Chart options filled
for (var info of infos_gantt) {
    let start = info["start"];
    let end = info["end"];
    options.series[0].data.push({
        name: info["name"],
        start: Date.UTC(start[0], start[1], start[2]),
        end: Date.UTC(end[0], end[1], end[2]),
    })
}

// On affiche le chart
Highcharts.ganttChart('gantt', options);