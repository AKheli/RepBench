const injectedSeries = []
const repairedSeries = []

// const normalized_series = new Map() // series -> normdata

const original_data_map = new Map();
const norm_data_map = new Map();

let normalized = true

const addSeries = function (series) {
    const chartSeries = mainchart.addSeries(series)
    original_data_map.set(chartSeries.options.id, [...series.data])
    norm_data_map.set(chartSeries.options.id, [...series.norm_data])
    series.norm_data = -1
    set_series_state(chartSeries)
    return chartSeries
}


const set_series_state = function (ser) {
    if (norm_data_map.has(ser.options.id)) {
        if (normalized) {
            ser.update({data: norm_data_map.get(ser.options.id)})
        } else {
            ser.update({data: original_data_map.get(ser.options.id)})
        }
    }
}

const swap_norm = function () {
    normalized = !normalized
    mainchart.series.forEach(ser => set_series_state(ser))
}


const addOriginalSeries = function (series) {
    addSeries(series)
}
const addInjectedSeries = function (series) {
    // add series to injectedSeries and main chart keep track of index of the series
    let chartSeries = addSeries(series)
    series['chartId'] = chartSeries.options.id
    injectedSeries.push(series)
    return chartSeries.color
}

const addRepairedSeries = function (series, col) {
    console.log("series",series)
    let chartSeries = null
    if (col === null) {
        chartSeries = addSeries(series)
        col = chartSeries.color
        series['color'] = col
    } else {
        series['color'] = col
        chartSeries = addSeries(series)
    }
    series['chartId'] = chartSeries.options.id
    repairedSeries.push(series)
    return col
}

// let clearInjectedSeries = function () {
//     for (let i = 0; i < injectedSeries.length; i++) {
//         mainchart.get(injectedSeries.chartId).remove(false);
//     }
//     injectedSeries.length = 0 // is that rally smart?
// }
//
// let clearRepairedSeries = function () {
//     for (let i = 0; i < repairedSeries.length; i++) {
//         mainchart.get(repairedSeries.chartId).remove(false);
//     }
//     repairedSeries.length = 0
// }
//
// let clearAllSeries = function () {
//     clearInjectedSeries()
//     clearRepairedSeries()
// }
