let optChart = null
let initOptChart = function (params, error) {
    optChart = Highcharts.chart('optChartContainer', {
            legend: {
                align: 'right',
                verticalAlign: 'top',
                floating: true
            },
            xAxis: {
                labels: {
                     tickInterval: 1,
                }
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
