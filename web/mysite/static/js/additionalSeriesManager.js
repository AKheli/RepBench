
let injectedSeries = []
let repairedSeries = []

let addInjectedSeries = function(series) {
    // add series to injectedSeries and main chart keep track of index of the series
    chartSeries = mainchart.addSeries(series)
    series['chartId'] = chartSeries.options.id
    injectedSeries.push(series)
}

let addRepairedSeries = function(series) {
    chartSeries = mainchart.addSeries(series)
    series['chartId'] = chartSeries.options.id
    repairedSeries.push(series)
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
