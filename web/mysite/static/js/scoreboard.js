let score_chart = null
let runtime_chart = null

// display text in the center of div container2
document.getElementById('score-container').innerHTML = "<h4 style='text-align:   ;margin-top:20px;'>Inject and then repair a <br> TimeSeries to display scores</h4>"

initScoreChart = function (series) {
    document.getElementById('score-container').innerHTML = ""
    score_chart = Highcharts.chart('score-container', {
        chart: {
            type: 'column',
        },
        title: {
            text: '',
        },
        xAxis: {
            categories: ["MAE", "RMSE", "RMSE on Anomaly"]
        },
        yAxis: {
            title: {
                text: 'Score'
            }

        },
        series: [series]
    });
    return score_chart.series[0]
}

initRuntimeChart = function (series) {
    runtime_chart = Highcharts.chart('runtime-container', {
        chart: {
            type: 'column',
        },
        title: {
            text: '',
        },
        xAxis: {
            categories: ["Runtime"]
        },
        yAxis: {
            type: 'logarithmic',

            title: {
                text: 'time(s)'
            }

        },
        series: [series]
    });
    return runtime_chart.series[0]
}


const bindSeriesMouseOver = function (score_series,runtime_series, repair_series) {
    const f = function () {
                mainChart.series.forEach(s => s.setVisible(false))
                repair_series.forEach(chartSeries => {
                    let injected_series = chartSeries.linkedParent
                    let truth_series = injected_series.linkedParent
                    injected_series.update({visible: true})
                    truth_series.update({visible: true})
                    chartSeries.setVisible()
                })
            }
    score_series.update({
        events: {
            click: f
        }
    })
    runtime_series.update({
        events: {
            click: f
        }
    })

}


const addScores = function (scores, rapiredSeries) {
    let score_series = null
    let runtime_series = null
    scores["colorByPoint"] = false
    if (score_chart == null) {
        const runtime = scores.data.data[3]
        scores.data = scores.data.data.filter((d, i) => i < 3) // remove runtime
        score_series = initScoreChart(scores)
        scores.data = [runtime]
        runtime_series = initRuntimeChart(scores)
        const element = document.getElementById("chart-right");

        // setTimeout(
        //     function () {
        //     //     element.animate({
        //     //         scrollTop: element.scrollHeight
        //     //     }, 500);
        //         // element.scrollTop = element.scrollHeight;
        // element.scrollIntoView({ behavior: 'smooth', block: 'end' });
        //     }, 1000);
        element.scrollIntoView({ behavior: 'smooth', block: 'end' });

    } else {
        const runtime = scores.data.data[3]
        scores.data = scores.data.data.filter((d, i) => i < 3) // remove runtime
        score_series = score_chart.addSeries(scores)
        scores.data = [runtime]
        runtime_series = runtime_chart.addSeries(scores)
    }

    bindSeriesMouseOver(score_series,runtime_series, rapiredSeries)


}

const removeScores = function () {
    if(score_chart !== null){
        score_chart.destroy()
    }
    score_chart = null
    if(runtime_chart !== null){
        runtime_chart.destroy()
    }
    runtime_chart = null
    document.getElementById('score-container').innerHTML = "<h4 style='text-align:   ;margin-top:20px;'>Inject and then repair a <br> TimeSeries to display scores</h4>"
}
