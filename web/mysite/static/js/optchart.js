let optChart = null
let initOptChart = function (params, error, n_init, n_sample) {
    optChart = Highcharts.chart('optChartContainer', {
            chart: {
                marginRight: 0
            },

            legend: {
                align: 'right',
                verticalAlign: 'top',
                layout: 'vertical',
                x: 0,
                y: 10
            },

            tooltip: {
                shared: true,
                crosshairs: true
            },
            xAxis: {
                label: {
                    text: 'Iteration',
                    style: {
                        "font-size": "15px",
                        transform: "translate(0, -37px)"
                    },
                },
                plotBands: [{
                    color: 'rgba(3, 11, 12, 0.2)',// Color value
                    from: 0, // Start of the plot band
                    to: n_init, // End of the plot band
                    label: {
                        text: 'Initial Sampling',
                        verticalAlign: 'middle',
                        y: -1,
                        style: {
                            "font-size": "15px",
                            // transform: "translate(0, -21px)"

                        }

                    }, // Content of the label
                }, {
                    color: 'rgba(3, 11, 12, 0.2)',// Color value
                    from: n_init + 1, // Start of the plot band
                    to: n_init + n_sample, // End of the plot band
                    label: {
                        text: 'Maximum Expectation Sampling',
                        verticalAlign: 'middle',
                        style: {
                            "font-size": "15px",
                            // transform: "translate(0, -37px)"
                        }

                    }, // Content of the label
                }],
                labels: {
                    tickInterval: 1,
                    start: 1

                },
                max: n_init + n_sample,
            },
            title: {
                text: '',
            },
            yAxis: [{
                title: {
                    text: 'Parameters'
                },
                height: '45%',
                lineWidth: 2
            }, {
                title: {
                    text: error
                },
                top: '50%',
                height: '50%',
                offset: 0,
                lineWidth: 2
            }],
            series: params.map(param => {
                console.log(param)
                return {
                    type: 'line',
                    name: param,
                    yAxis: 0,
                    data: []
                }
            }).concat([{
                //error chart
                showInLegend: false,
                type: 'line',
                // name: error,
                color: 'red',
                data: [],
                yAxis: 1,

            }])

        }
    );

    optChart.addParamError = function (params, error) {
        params.forEach((param, i) => {

            optChart.series[i].addPoint(param);
        })
        optChart.series[optChart.series.length - 1].addPoint(error)

    }
}
