Highcharts.setOptions({
    plotOptions: {
        series: {
            animation: false
        }
    }
});

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

let range_selector = {
    buttons: [{
        count: 1,
        text: '1m',
        events: {
            click: function () {
                alert('Clicked button');
            }
        }
    },
        {
            count: 3,
            text: '3m'
        }
    ],
    enabled: true,
}

let mainChart = null
let threshold = null


let splitMainChart = function () {

    return [{
        title: {
            text: 'Parameters'
        },
        height: '53%',
        lineWidth: 2,
    }, {
        title: {
            text: "Normalized Difference"
        },
        top: '57%',
        height: '43%',
        offset: 0,
        lineWidth: 2,
        min: -1,
        max: 10,
        // }], series: mainChart.series.concat([{
        //     //error chart
        //     showInLegend: false,
        //     type: 'line',
        //     color: 'red',
        //     data: [1, 3, 4, 5, 6, 7],
        yAxis: 1,
    }]
}


const initMainChart = function (series = {}) {
    mainChart = Highcharts.chart(document.getElementById('highcharts_container'), {
        // dataGrouping: {
        //     enabled: false
        // },

        legend: {
            enabled: true,

            align: 'right',
            verticalAlign: 'top',
            // floating: true,
            // x: 0,
            y: 30
        },
        tooltip: tooltip,
        chart: {
            type: 'line',
            zoomType: 'x',
            animation: false,
        },
        yAxis: threshold === null ? [{}, {
            title: {
                text: ""
            },
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


        navigator: {
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
        },

        rangeSelector: {
            inputDateParser: function (value) {
                console.log(value)
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
                    x: 0,
                    y: 100,
                }],
        },

        series: series,


    });

    if(threshold !== null){
        mainChart.yAxis[1].addPlotLine(
        {
            color: '#FF0000',
            width: 1,
            style: "dash",
            value: threshold,
            yAxis: 1,
            label: {
                text: 'Threshold',
                align: 'right',
                x: -10
            }
        }
    )
    }
}

fetch(data_url, {
    method: 'GET',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': '{{ csrf_token }}'
    }
}).then(response => response.json())
    .then(data => {
        data.series.forEach(x => addOriginalSeries(x))
        resetSeries()
    }).catch(error => console.error(error))



