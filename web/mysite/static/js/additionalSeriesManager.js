let injectedSeries = []
const repairedSeries = []
const originalSeries = []

let normalized = false
const addSeries = function (series) {
    const chartSeries = mainChart.addSeries(series)
    let ser = {
        series: series,
        chartSeries: chartSeries,
        originalData: [...series.data],
        normData: [...series.norm_data]
    }
    set_series_state(ser)
    return ser
}

const set_series_state = function (ser) {
    ser.chartSeries.update({data: normalized ? ser.normData : ser.originalData})
}

const swap_norm = function () {
    normalized = !normalized
    document.getElementById("swap_norm").innerHTML
        = normalized ? "Show Original Data" : "Normalize Data"

    injectedSeries.forEach(ser => set_series_state(ser))
    repairedSeries.forEach(ser => set_series_state(ser))
    originalSeries.forEach(ser => set_series_state(ser))
}


const get_injected_norm_data = function () {
    //data that gets sent to the back end
    return injectedSeries.map(s => {
        return {
            linkedTo: s.series.linkedTo,
            id: s.series.id, //injected id
            data: s.series.norm_data
        }
    })
}

const addOriginalSeries = function (series) {
    originalSeries.push(addSeries(series))
}

const addInjectedSeries = function (series, previously_injected) {
    console.log(previously_injected)
    if (previously_injected) {
        console.log("previously injected")
        series.data.forEach((p, i) => {
            if (series.data[i] === null) {
                if (previously_injected.originalData[i] !== null) {
                    series.data[i] = previously_injected.originalData[i]
                    series.norm_data[i] = previously_injected.normData[i]
                }
            }

        })
    }
    const retval = addSeries(series)
    injectedSeries.push(retval)


    return retval.chartSeries.color
}

const addRepairedSeries = function (series, col) {
    let retval = null
    if (col === null) {
        retval = addSeries(series)
        col = retval.chartSeries.color
    } else {
        series.color = col
        retval = addSeries(series)

    }
    repairedSeries.push(retval)

    return {color: col, series: retval.chartSeries}
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

