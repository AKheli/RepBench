let tooltip = {
    formatter: function (e) {
        // The first returned item is the header, subsequent items are the
        // points
        let x = this.x
        return ['<p style=\"color:black;font-size:15px;\"> Truth: ' + this.y + '</p>'].concat(
            this.series.linkedSeries.map(function (s) {
                selectedY = s.yData[x]
                if (selectedY !== null) {
                    selectedY = Math.round(selectedY * 1000) / 1000
                    if (s.name.includes('injected')) {
                        return "<br> <p style=\"color:red;font-size:15px;\"> Anomalous: " + selectedY + "<\p> "
                    } else return "<br> <p style=\"color:" + s.color + ";font-size:15px;\">" + s.name + ": " + selectedY + "<\p> "
                } else return ""
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


const mainChart = Highcharts.chart(document.getElementById('highcharts_container'), {
      legend: {
          nabled: true,

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
    },

    // {#xAxis: {#}
    // {#    labels: {#}
    // {#          pointInterval: 36e5, // one hour#}
    // {#relativeXValue: true,#}
    // {#        formatter: function () {#}
    // {#            console.log("v" + this.value)#}
    // {#            return this.value.toString();#}
    // {#        },#}
    // {#    }#}


    plotOptions: {
        series: {
            pointStart: 1,
            pointInterval: 36e5, // one hour

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

    series: {}
});

fetch(data_url, {
    method: 'GET',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': '{{ csrf_token }}'
    }
}).then(response => response.json())
    .then(data => {
        data.series.forEach(x => addOriginalSeries(x))
    })
    .catch(error => console.error(error))

