let flamlChart = null



function initFlamlChart(estimators) {
    console.log("init flaml chart")
    flamlChart = Highcharts.chart('flaml-chart', {
        // chart: {
        //     type: 'column',
        //     // height: 290,
        // },
        title: {
            text: ''
        },
        xAxis: {
            // categories: []
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Score'
            }
        },
        // tooltip: {
        //     pointFormat: '<span style="color:{series.color}">{series.name}</span>: <b>{point.y}</b> ({point.percentage:.0f}%)<br/>',
        //     shared: true
        // },
        // plotOptions: {
        //     column: {
        //         stacking: 'normal'
        //     }
        // },
        // series: [{}]estimators.map(e => {
        //     return {
        //         name: e,
        //         data: []
        //
        //     }
        // })
        series : [{ data:[] , name: "score" }]

    });

}

function addDataToFlamlChart(score, classifier, time) {
    let categories = flamlChart.xAxis[0].categories
    categories.push(time)
    flamlChart.xAxis[0].setCategories(categories, false);
    // iterate series
    flamlChart.series.forEach(function (series, i) {
        console.log(series.name , classifier)
        series.addPoint(classifier === series.name ? score : 0 , false);
    })
}