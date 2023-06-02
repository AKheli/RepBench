let flamlChart = null


function initFlamlChart(estimators) {
    console.log("init flaml chart")
    flamlChart = Highcharts.chart('flaml-chart', {
        chart: {
            type: 'column',
            // height: 290,
        },
        title: {
            text: ''
        },
        xAxis: {
            categories: [""],
            plotLines: [{
                color: 'red',
                width: 3,
                value: 0.5,
                dashStyle: "dot"
            }]
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Test Score'
            }
        },

        plotOptions: {
            column: {
                // grouping: false,
                // shadow: false,
                borderWidth: 0
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
        series: [{name: "current", data: [0] , showInLegend: false}]
        // series: [{data: [], name: "" , showInLegend: false, type: "line"}]

    });


    flamlChart.presentationMode = "split" //or combined
    flamlChart.addData = function (score, estimator, iter) {
        let categories = flamlChart.xAxis[0].categories
        if (!categories.includes(estimator)) {
            flamlChart.xAxis[0].setCategories([...categories, estimator]);
            flamlChart.series.filter(s => s.name === "current")[0].addPoint(score)

            // flamlChart.series.filter(s => s.name === "best")[0].addPoint(score)

        } else {
            let seriesData = flamlChart.series.filter(s => s.name === "current")[0].data
            seriesData[categories.indexOf(estimator)].update(score)
            let best = seriesData[0]
            if(score > best.y) {
                best.update({color: "red" , y: score})
                categories[0] = "<b>" + estimator+ "</b>"
            }
            // const currentBest = flamlChart.series.filter(s => s.name === "best")[0].data[categoreis.indexOf(estimator)].y
            console.log("estimator", estimator)
            // console.log("currentBest", currentBest)
            console.log("score", score)
            // if (currentBest < score) {
            //     flamlChart.series.filter(s => s.name === "best")[0].data[categoreis.indexOf(estimator)].update(score)
            // }
            // let arr = flamlChart.series.filter(s => s.name === "best")[0].data.map(d => d.y);
            // let max = Math.max(...arr);
            // let maxIndex = arr.indexOf(max);
            // flamlChart.series.filter(s => s.name === "best")[0].data.forEach((d, i) => {
            //     if (i === maxIndex) {
            //         d.update({color: "red"})
            //     } else {
            //         d.update({color: "blue"})
            //     }
            // })
        }

        // if (this.presentationMode === "split") {
        //     const targetSeries = flamlChart.series.filter(s => s.name === estimator)
        //     console.log(targetSeries, "targetSeries")
        //     if (targetSeries.length === 0) {
        //         flamlChart.addSeries({name: estimator, type:"column", data: [{x: iter, y: score}]})
        //         flamlChart.categories.push(estimator)
        //     } else {
        //         targetSeries[0].addPoint({x: iter, y: score})
        //     }
        // } else {
        //     flamlChart.series[0].addPoint({name: estimator, x: iter, y: score})
        // }
    }

    flamlChart.toggle = function () {
        if (flamlChart.series.length === 0) { //combined case
            const distinctEstimators = [...new Set(flamlChart.series[0].data.map(d => d.name))];
            const estimatorSeries = []
            const newSeries = distinctEstimators.map(estimator => {
                return {
                    name: estimator,
                    data: flamlChart.series[0].data.filter(d => d.name === estimator)
                }
            })
            flamlChart.series[0].remove()
            newSeries.forEach(n => flamlChart.addSeries(n))
        } else { //combine the chart
            const newSeries = {name: "combined", data: []}
            const combinedSeries = [].concat(...flamlChart.series.map(s => s.data))
            for (let i in flamlChart.series.length) {
                flamlChart.series.remove()
            }
            flamlChart.addSeries(combinedSeries)
        }
    }
}

// function addDataToFlamlChart(score, classifier, time) {
//     let categories = flamlChart.xAxis[0].categories
//     categories.push(time)
//     flamlChart.xAxis[0].setCategories(categories, false);
//     // iterate series
//     flamlChart.series.forEach(function (series, i) {
//         console.log(series.name, classifier)
//         series.addPoint(classifier === series.name ? score : 0, false);
//     })
// }