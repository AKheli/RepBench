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
    console.log(series)
    return score_chart2.series[0]
}


allScores = {}
const seriesMap = [];
let selectedCategoires = new Set()

updateCategories = function () {
    console.log("map")
    console.log(seriesMap)
    seriesMap.forEach( e  => {
            console.log("E1")
            console.log(e[1])
            e[0].update({data: e[1].filter(d => selectedCategoires.has(d.name))})
        }
    )
}



addScores = function (scores) {
    scores["colorByPoint"] = false
    if (score_chart2 == null) {
        series = initChart(scores)
        let scoresData = scores.data.data
        seriesMap.push( [series, scoresData] )
        console.log(scoresData)
        scoresData.forEach(datapoint => alterCheckbox(datapoint.name))

    } else {
        series = score_chart2.addSeries(scores)
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

//  = function(categories){
//     checkbox = document.getElementById('score-checkbox')
//     checkbox.appendChild(document.createElement.)
// }

// <div className="form-check form-check-inline">
//     <input className="form-check-input" type="checkbox" onSelect="">
//         <label className="form-check-label" htmlFor="inlineCheckbox1">1</label>
// </div>
