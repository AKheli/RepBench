let injectedSeries = []
const repairedSeries = []
const originalSeries = []
const reducedSeries = []

let normalized = false

const addSeries = function (series) {
    let ser = {
        series: series,
        chartSeries: null,
        originalData: [...series.data],
        normData: [...series.norm_data]
    }
    return ser
}


const swap_norm = function () {
    normalized = !normalized
    resetSeries()

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

const addReducedSeries = function (series) {
    reducedSeries.push(addSeries(series))
}

const addInjectedSeries = function (series, previously_injected) {
    if (previously_injected) {
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
}

const addRepairedSeries = function (series, col) {

    if (col != null) {
        series.color = col
        repairedSeries.push(addSeries(series))
    } else {
        repairedSeries.push(addSeries(series))

    }
}


const clearAllSeries = function () {
    while (mainChart.series.length > originalSeries.length) {
        mainChart.series[originalSeries.length].remove(false)
    }
    repairedSeries.length = 0
    injectedSeries.length = 0
    reducedSeries.length = 0
    mainChart.redraw()
    removeScores()
}

const resetSeries = function () {
    let allSeries = originalSeries.concat(injectedSeries).concat(repairedSeries).concat(reducedSeries)
    allSeries.forEach(s => {
        s.series.data = normalized ? [...s.normData] : [...s.originalData]
    })
    let allInputSeries = allSeries.map(s => s.series)
    initMainChart(allInputSeries)
    allSeries.forEach((s, i) => s.chartSeries = mainChart.series[i])
}
