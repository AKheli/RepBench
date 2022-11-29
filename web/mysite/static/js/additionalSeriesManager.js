let injectedSeries = []
const repairedSeries = []

const original_data_map = new Map();
const norm_data_map = new Map();

let normalized = true

const addSeries = function (series) {
    const chartSeries = mainChart.addSeries(series)
    original_data_map.set(chartSeries.options.id, [...series.data])
    norm_data_map.set(chartSeries.options.id, [...series.norm_data])
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
    document.getElementById("swap_norm").innerHTML
        = normalized ? "Show Original Data" : "Normalize Data"

    mainChart.series.forEach(ser => set_series_state(ser))
}


const get_injected_norm_data = function () {
    return injectedSeries.map(s => {
        return {
            linkedTo: s.series.linkedTo,
            data: s.series.norm_data
        }
    })
}

const addOriginalSeries = function (series) {
    addSeries(series)
}
const addInjectedSeries = function (series) {
    // add series to injectedSeries and main chart keep track of index of the series
    let chartSeries = null
    chartSeries = addSeries(series)
    console.log("charts",chartSeries)
    series['chartId'] = chartSeries.options.id
    injectedSeries.push({series: series, "chartSeries": chartSeries})
    return chartSeries.color
}

const addRepairedSeries = function (series, col) {
    let chartSeries = null
    if (col === null) {
        chartSeries = addSeries(series)
        col = chartSeries.color
        series['color'] = col
    } else {
        series['color'] = col
        chartSeries = addSeries(series)
    }
    series['chartId'] = "" + chartSeries.options.id
    repairedSeries.push({series: series, chartSeries: chartSeries})

    return col
}


const clearRepairedSeries = function () {
    repairedSeries.forEach(s => s.chartSeries.remove())
    repairedSeries.length = 0
}

const clearInjectedSeries = function () {
    injectedSeries.forEach(s => s.chartSeries.remove())
    injectedSeries.length = 0
    collapseRepairToggle()
}
const clearAllSeries = function () {
    clearRepairedSeries()
    clearInjectedSeries()
}

