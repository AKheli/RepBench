var score_chart2 = null;

initChart = function (series) {
    score_chart2 = Highcharts.chart('container2', {
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

    // score_chart2.renderer.text('This text is background text', 150, 200)
    //     .css({
    //         color: '#4572A7',
    //         fontSize: '16px'
    //     })
    //     .add();

    return score_chart2.series[0]
}


allScores = {}
const seriesMap = new Map();

x = 0
selectedCategoires = new Set()

updateCategories = function () {
    seriesMap.forEach((originaldata, series) => {
            series.update({data: originaldata.filter(d => selectedCategoires.has(d.name))})
        }
    )
}

addScores = function (scores) {
    if (score_chart2 == null) {
        series = initChart(scores)
        // series = score_chart2.addSeries(scores)
        seriesMap.set(series, scores.data)
        scores.data.forEach(datapoint => alterCheckbox(datapoint.name))

    } else {
        series = score_chart2.addSeries(scores)
        seriesMap.set(series, scores.data)
    }

    updateCategories()

}

alterCheckbox = function (category) {
    console.log()
    if (selectedCategoires.has(category)) selectedCategoires.delete(category);
    else selectedCategoires.add(category)
    updateCategories()
}

//  = function(categories){
//     checkbox = document.getElementById('score-checkbox')
//     checkbox.appendChild(document.createElement.)
// }

// <div className="form-check form-check-inline">
//     <input className="form-check-input" type="checkbox" onSelect="">
//         <label className="form-check-label" htmlFor="inlineCheckbox1">1</label>
// </div>
