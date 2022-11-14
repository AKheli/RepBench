score_chart = null

initChart = function (series) {
    score_chart = Highcharts.chart('container2', {
        chart: {
            type: 'column',
        },
        title: {
            text: '',
        },
        xAxis: {
            type: 'category'
        },
        yAxis: {
            title: {
                text: 'score'
            }

        },
                series: [series]
    });
    return score_chart.series[0]
}


allScores = {}
const seriesMap = [];
let selectedCategoires = new Set()

updateCategories = function () {
    seriesMap.forEach( e  => {
            e[0].update({data: e[1].filter(d => selectedCategoires.has(d.name))})
        }
    )
}



addScores = function (scores) {
    scores["colorByPoint"] = false
    if (score_chart == null) {
        series = initChart(scores)
        let scoresData = scores.data.data
        seriesMap.push( [series, scoresData] )
        console.log(scoresData)
        scoresData.forEach(datapoint => alterCheckbox(datapoint.name))

    } else {
        series = score_chart.addSeries(scores)
        seriesMap.push( [series, scores.data.data] )
    }

    updateCategories()

}

alterCheckbox = function (category) {
    console.log()
    if (selectedCategoires.has(category)) selectedCategoires.delete(category);
    else selectedCategoires.add(category)
    updateCategories()
}


