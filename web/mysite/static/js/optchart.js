let optChart = null
let initOptChart = function (params, error) {
    optChart = Highcharts.chart('optChartContainer', {
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
            type: 'line',
            name: error,
            color: 'red',
            data: [],
            yAxis: 1
        }])

    });

    optChart.addParamError = function (params, error) {
        console.log("adding param error")
        console.log(params)
        console.log(optChart.series)
        params.forEach((param, i) => {
            console.log("data")
            console.log(optChart.series[i].data)
            optChart.series[i].addPoint(param);
        })
        console.log("error")
        console.log(error)
        optChart.series[optChart.series.length - 1].addPoint(error)

    }
}
