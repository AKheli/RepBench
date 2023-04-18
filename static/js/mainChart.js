Highcharts.setOptions({
    plotOptions: {
        series: {
            animation: false
        }
    }
});



const chartNavigator = { // do not use navigator since it is used by another script
    xAxis: {
        labels: {
            formatter: function () {
                return this.value.toString();
            }
        }
    },
    enabled: true,
    adaptToUpdatedData: true,
    height: 60
}

// All series that are not part of the original graph have to be linked to some other series
const events = {
    // hide linked series elements
    render: function () {
        let series = this.series

        if (series.filter(s => s.visible).length === 0) {
            series[0].show()
        }

        series.forEach(s => {
            var id = s.userOptions.id,
                name = s.userOptions.name
            var boundedId = Array.from(document.getElementsByClassName(id + "-bounded"))
            var boundedName = Array.from(document.getElementsByClassName(name + "-bounded"));
            // concatenate boundedId and boudedName
            var bounded = boundedId.concat(boundedName);
            if (bounded.length > 0) {
                if (s.visible) {
                    bounded.forEach(b => {
                        b.style.display = "block";
                    })
                } else {
                    bounded.forEach(b => {
                        b.style.display = "none";
                    })
                }
            }

        })
    },

}


let tooltip = {
    formatter: function (e) {
        // The first returned item is the header, subsequent items are the
        // points
        let x = this.x
        return ['<p style=\"color:black;font-size:15px;\"> ' + this.series.name + ': ' + this.y + '</p>'].concat(
            this.series.linkedSeries.map(function (s) {
                selectedY = s.data[x].y
                selectedY = Math.round(selectedY * 1000) / 1000
                if (selectedY !== null) {
                    if (s.name.includes('injected')) {
                        return "<br> <p style=\"color:red;font-size:15px;\">" + s.name + " " + selectedY + "<\p> "
                    } else return "<br> <p style=\"color:" + s.color + ";font-size:15px;\">" + s.name + ": " + selectedY + "<\p> "
                }

            })
        );
    },
    shared: false,
    valueDecimals: 2
}


let mainChart = null
let threshold = null

let legendWidth = null

let load_chart = null
const loadChart = function (series = {}, container = 'load_chart') {
    document.getElementById("content").style["overflow-y"] = "hidden"
    if (load_chart !== null) {
        load_chart = null
    }
    load_chart = Highcharts.chart(document.getElementById("load_chart"), {
        series: [{data: [], showInLegend: false}],
        title: {
            text: chart_title,
            style: {
                color: 'black',
                fontWeight: 'bold',
                "font-size": "30px"
            }
        },
        credits: {
            enabled: false
        },
    })
    load_chart.showLoading('<img src="https://upload.wikimedia.org/wikipedia/commons/b/b1/Loading_icon.gif">');
}
loadChart()


const initMainChart = function (series = {}, container = 'highcharts_container') {
    mainChart = Highcharts.chart(document.getElementById(container), {
        credits: {
            enabled: false
        },
        legend: {
            enabled: true,
            align: 'right',
            verticalAlign: 'top',
            floating: true,
            // y :-20,
            // x : -20,
            width:legendWidth
        },
        tooltip: tooltip,
        chart: {
            type: 'line',
            zoomType: 'x',
            animation: false,
            events: events,
            // spacingTop: 20
            x: -200,
        },
        yAxis: threshold === null ? [{
            title: {
                text: "",
            },
            endOnTick: true,
        }] : splitMainChart(),
        plotOptions: {
            series: {
                pointStart: 1,
                pointInterval: 1,
                series: {
                    marker: {
                        enabled: false,
                        states: {
                            hover: {
                                enabled: false
                            }
                        }
                    },
                    shadow: false,
                    animation: false
                }
            },
        },

        title: {
            text: chart_title,
            style: {
                color: 'black',
                fontWeight: 'bold',
                "font-size": "30px"
            }
        },

        navigator: chartNavigator,
        rangeSelector: {
            x: 0,
            // floating: true,
            style: {
                color: 'black',
                fontWeight: 'bold',
                position: 'relative',
                "font-family": "Arial"
            },
            inputDateParser: function (value) {
                value = value.split(/[:\.]/);
                return 1
            },
            enabled: true,
            inputEnabled: false,
            inputDateFormat: '%y',
            inputEditDateFormat: '%y',
            buttons: [{
                type: 'millisecond',
                count: 50,
                text: '50'
            },
                {
                    type: 'millisecond',
                    count: 1000,
                    text: '1000'
                }, {
                    type: 'all',
                    text: 'All',
                    align: 'right',
                    x: 1000,
                    y: 100,
                }],
        },

        series: series, // add a series otherwise it does not work
    });
}

const mainChartFetchPromise = new Promise((resolve, reject) => {
    fetch(data_url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}'
        }
    }).then(response => response.json())
        .then(data => {
            if (data.injected) {
                initMainChart(data.series.concat(data.injected))
            } else {
                initMainChart(data.series)
            }

            // Store data
            data.series.forEach(s => addOriginalSeries(s))
            if (data.injected) {
                data.injected.forEach(s => addInjectedSeries(s))
            }
            resetSeries()
            load_chart.hideLoading()
            document.getElementById("load_chart").style.display = "none";
            document.getElementById("content").style["overflow-y"] = "auto"
            resolve()


        }).catch(error => console.error(error))
})


