const injectedSeries = []
const repairedSeries = []


const normalizationState = false

const addInjectedSeries = function(series) {
    // add series to injectedSeries and main chart keep track of index of the series
    chartSeries = mainchart.addSeries(series)
    series['chartId'] = chartSeries.options.id
    injectedSeries.push(series)
    return chartSeries.color
}

const addRepairedSeries = function(series,col) {
    let chartSeries = null
    if(col === null){
        console.log(series)
        chartSeries = mainchart.addSeries(series)
        col = chartSeries.color
        series['color'] = col
    }
    else{
        series['color'] = col
        chartSeries = mainchart.addSeries(series)
    }

    series['chartId'] = chartSeries.options.id
    repairedSeries.push(series)
    return col
}

let clearInjectedSeries = function() {
     for (let i = 0; i < injectedSeries.length; i++) {
       mainchart.get(injectedSeries.chartId).remove(false);
    }
    injectedSeries = []
}

let clearRepairedSeries = function() {
    for (let i = 0; i < repairedSeries.length; i++) {
       mainchart.get(repairedSeries.chartId).remove(false);
    }
    repairedSeries = []
}

let clearAllSeries = function() {
    clearInjectedSeries()
    clearRepairedSeries()
}
