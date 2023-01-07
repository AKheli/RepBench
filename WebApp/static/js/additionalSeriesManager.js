let injectedSeries = []
const repairedSeries = []
const originalSeries = []
const reducedSeries = []

let normalized = false


const addSeries = function (series) {
    let ser = {
        series: series,
        chartSeries: null,
        originalData: series.data.map(s => s),
        normData: series.norm_data.map(s => s)
    }
    return ser
}


const swap_norm = function () {
    normalized = !normalized
    document.getElementById("swap_norm").innerHTML = normalized ? "Show Original Data" : "Normalize Data"
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
    const retval = addSeries(series)
    originalSeries.push(addSeries(series))
    return retval
}

const addReducedSeries = function (series) {
    const retval = addSeries(series)
    reducedSeries.push(retval)
    return retval
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
    return retval
}

const addRepairedSeries = function (series, col) {
    if (col != null) {
        series.color = col
    }
    const retval = addSeries(series)
    repairedSeries.push(retval)
    return retval
}


const clearAllSeries = function () {
    repairedSeries.length = 0
    injectedSeries.length = 0
    reducedSeries.length = 0
    threshold = null
    resetSeries()
    removeScores()

}


const resetSeries = function (showOnlyInjected = false) {
    let allSeries = originalSeries.concat(injectedSeries).concat(repairedSeries).concat(reducedSeries)

    if (showOnlyInjected) {
        const repairLinks = injectedSeries.map(s => {
            return s.series.linkedTo
        })
        originalSeries.forEach(o => {
            o.series.visible = repairLinks.includes(o.series.id)
        })
    }

    allSeries.forEach(s => {
        console.log(normalized)
        s.series.data = normalized ? [...s.normData] : [...s.originalData]
        if(s.chartSeries && !showOnlyInjected){
            s.series.visible = s.chartSeries.visible
        }
    })
    let allInputSeries = allSeries.map(s => s.series)
    initMainChart(allInputSeries)
    allSeries.forEach((s, i) => s.chartSeries = mainChart.series[i])

}


let injectedString = null
const stringifyInjectedSeries = function () {
    injectedSeries.forEach(s => {
        s.series.data = s.originalData
    })
    injectedString = JSON.stringify(injectedSeries.map(s => s.series))
}

const loadInjectedSeries = function () {
    if (injectedString) {
        let loadedInjected = JSON.parse(injectedString)
        loadedInjected.forEach(s => {
            addInjectedSeries(s)
        })
        resetSeries()

    }

}


$('#rawButton').click(function () {

    $('#zButton').removeClass('active');
    // $('#minMaxButton').removeClass('active');
    $('#rawButton').addClass('active');
    normalized = false;
    resetSeries()
})

$('#zButton').click(function () {
    console.log("normalized")
    $('#rawButton').removeClass('active');
    // $('#minMaxButton').removeClass('active');
    $('#zButton').addClass('active');
    if (!normalized) {
        normalized = true;
        resetSeries()
    }
});
