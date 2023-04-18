const createProbabilityChart = function (probabilities) {
    var data = Object.keys(probabilities).map(function (key) {
        return {
            name: key,
            y: probabilities[key]
        }
    })
// Create the chart using Highcharts
    Highcharts.chart('probabilities-chart', {
        chart: {
            type: 'column'
        },
        title: {
            text: ''
        },
            credits: {
            enabled: false
        },
        xAxis: {
            categories: Object.keys(probabilities),
            title: {
                text: 'Algorithm'
            }
        },
        yAxis: {
            min: 0,
            max: 1,
            title: {
                text: 'Probability'
            }
        },
        plotOptions: {
            column: {
                dataLabels: {
                    enabled: true,
                    format: '{point.y:.2f}'
                }
            }
        },
        series: [{
            showInLegend: false,
            name: 'Probability',
            data: data,
        }]
    });
}

const invertObj = function (originalObj) {
    const invertedObj = {};
    for (const key in originalObj) {
        if (Object.hasOwnProperty.call(originalObj, key)) {
            const innerObj = originalObj[key];
            for (const innerKey in innerObj) {
                if (Object.hasOwnProperty.call(innerObj, innerKey)) {
                    if (!invertedObj[innerKey]) {
                        invertedObj[innerKey] = {};
                    }
                    invertedObj[innerKey][key] = innerObj[innerKey];
                }
            }
        }
    }
    return invertedObj
}
const createErrorChart = function (alg_scores) {
    let series = Object.entries(alg_scores).map(([k, v]) => {
        return {
            name: k,
            data: Object.entries(v).map(([k, v]) => v)
        }
    })
    alg_scores = invertObj(alg_scores)
    let alg_categories = Object.keys(alg_scores)

    console.log(series)
    console.log(alg_categories)
    Highcharts.chart('alg-scores-chart', {
        chart: {
            type: 'column'
        },
        title: {
            text: 'Algorithm scores'
        },
        xAxis: {
            categories: alg_categories
        },
        yAxis: {
            title: {
                text: 'Score'
            }
        },
            credits: {
            enabled: false
        },
        legend: {
            enabled: true
        },
        plotOptions: {
            column: {
                pointPadding: 0.2,
                shadow: false,
                borderWidth: 0
            }
        },
        series: series
    });
}

