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


addScores = function (scores) {
    scores["colorByPoint"] = false
    if (score_chart == null) {
        const runtime = scores.data.data[3]
        scores.data = scores.data.data.filter((d, i) => i < 3) // remove runtime
        initScoreChart(scores)
        scores.data = [runtime]
        initRuntimeChart(scores)
        const element = document.getElementById("chart-right");
        element.scroll({
            top: 100,
            left: 100,
            behavior: 'smooth'
        });
    } else {
        const runtime = scores.data.data[3]
        scores.data = scores.data.data.filter((d, i) => i < 3) // remove runtime
        score_chart.addSeries(scores)
        scores.data = [runtime]
        runtime_chart.addSeries(scores)
    }


}

