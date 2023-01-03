let thresholdChart = null
let classificationReductionChart = null


let simultaneousChartZoomLock = false
const bindZoom = function (...charts) {
    let bindEvents = function (caller) {
        return function (event) {
            if (!simultaneousChartZoomLock) {
                simultaneousChartZoomLock = true
                charts.forEach(chart => {
                    if (chart !== caller) {
                        chart.xAxis[0].setExtremes(event.min, event.max, true, false)
                    }
                })
                simultaneousChartZoomLock = false
            }
        }
    }

    charts.forEach(chart => {
        chart.update({xAxis: {events: {setExtremes: bindEvents(chart)}}})
    })

}

const init_threshold_chart = function (series = [{
    data: [],
    showInLegend: false
}], container = 'thresholdChartContainer') {
    thresholdChart = Highcharts.chart(document.getElementById(container), {

        chart: {
            type: 'line',
            zoomType: 'x',
        },
        title: {
            text: "",
        },
        series: series,
        xAxis: {
            title: {}
        }
    });
    thresholdChart.updateThreshold = function (threshold) {
        thresholdChart.yAxis[0].addPlotLine({
            color: 'black',
            width: 2,
            value: threshold,
            yAxis: 2,
            label: {
                text: 'Threshold',
                align: 'right',
                x: -10
            }

        })
    }
    mainChartFetchPromise.then(() => {
            thresholdChart.xAxis[0].setExtremes(mainChart.xAxis[0].min, mainChart.xAxis[0].max)
            // add simultaneous zoom

        }
    )
}


const initClassificationReductionChart = function (series_array = [{
    data: [],
}], container = 'classificationReductionChartContainer') {

    classificationReductionChart = Highcharts.chart(document.getElementById(container), {

        chart: {
            type: 'line',
            zoomType: 'x',
        },
        title: {
            text: "",
        },
        series: series_array.flat(),
        xAxis: {
            title: {}
        }
    });

   mainChartFetchPromise.then(() => {
            classificationReductionChart.xAxis[0].setExtremes(mainChart.xAxis[0].min, mainChart.xAxis[0].max)
            bindZoom(mainChart, thresholdChart, classificationReductionChart)
        }
    )
}

const initRepairIterChart = function (series_array = [{
    data: [],
}], container = 'RepairIterChartContainer') {

    RepairIterChart = Highcharts.chart(document.getElementById(container), {

        chart: {
            type: 'line',
            zoomType: 'x',
        },
        title: {
            text: "",
        },
        series: series_array.flat(),
        xAxis: {
            title: {}
        }
    });

   mainChartFetchPromise.then(() => {
            classificationReductionChart.xAxis[0].setExtremes(mainChart.xAxis[0].min, mainChart.xAxis[0].max)
            bindZoom(mainChart, thresholdChart, classificationReductionChart,RepairIterChart)
        }
    )
}

init_threshold_chart()
initClassificationReductionChart()
initRepairIterChart()


