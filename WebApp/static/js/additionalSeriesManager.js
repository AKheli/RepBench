let normalized = false

let injectedSeries = []
const repairedSeries = []
const originalSeries = []
const reducedSeries = []

//large color palette excluding red good visible with white background
const colors = ['#7cb5ec', '#434348', '#90ed7d', '#f7a35c', '#8085e9',
    '#50394c', '#e4d354', '#8085e8', '#8d4653', '#91e8e1', '#7cb5ec', '#434348', '#90ed7d', '#f7a35c', '#8085e9']
// color palette for repaired series,different from the one used for original series
const repairedColors = ['#4040a1', '#405d27', '#f18973', '#36486b']
const getRepairedColor = function () {
    return repairedColors[repairedSeries.length % repairedColors.length]
}
const getColor = function () {
    return colors[originalSeries.length % colors.length]
}



const chartSeriesMap = function (){
    let allSeries = originalSeries.concat(injectedSeries).concat(repairedSeries).concat(reducedSeries)
    var myDict = {};
    allSeries.forEach(s => {
        myDict[s.chartSeries.name] = s
    })
    return myDict
}

const normDataSelection = function (series) {
    return normalized ? [...series.normData] : [...series.originalData]
}
const swap_norm = function () {
    const seriesMap = chartSeriesMap()
    mainChart.series.forEach(s => {
        if(s.name in seriesMap){
            const series = seriesMap[s.name]
            s.setData(normDataSelection(series),false)
        }
    })
    mainChart.redraw()
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

const addSeries = function (series) {
    let ser = {
        series: series,
        originalData: series.data.map(s => s),
        normData: series.norm_data.map(s => s),
        name: series.name,
        chartSeries: null,
    }
    return ser
}
const addOriginalSeries = function (series , add_to_chart = false) {
    if (series.color == null) {
        series.color = getColor()
    }
    const retval = addSeries(series)
    originalSeries.push(retval)
    return retval
}


const addInjectedSeries = function (series, previously_injected) {
    console.log("ADD INJECTED SERIES")
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
    if (series.color == null) {
        series.color = getRepairedColor()
    }
    const retval = addSeries(series)
    repairedSeries.push(retval)
    return retval
}


const clearAllSeries = function () {
    repairedSeries.length = 0
    injectedSeries.length = 0
    reducedSeries.length = 0
    resetSeries()
    removeScores()
}


const resetSeries = function (showOnlyInjected = false) {
    console.log("resetSeries")
    if (mainChart !== null) {
        mainChart.showLoading('<img src="https://upload.wikimedia.org/wikipedia/commons/b/b1/Loading_icon.gif">');
    }
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
        if (s.chartSeries && !showOnlyInjected) {
            s.series.visible = s.chartSeries.visible
        }
    })

    let allInputSeries = allSeries.map(s => s.series)
    const axis0isDefined = mainChart !== null && mainChart.xAxis !== undefined && mainChart.xAxis[0] !== undefined


    if (axis0isDefined) {
        const chartMin = mainChart.xAxis[0].min+0
        const chartMax = mainChart.xAxis[0].max+0
        initMainChart(allInputSeries)
        mainChart.xAxis[0].setExtremes(chartMin, chartMax)
    }
    else {
        initMainChart(allInputSeries)
    }
    document.getElementById("highcharts_container_wrapper").style.display = "block"
    allSeries.forEach((s, i) => s.chartSeries = mainChart.series[i])
    updateExportInjectedButton(injectedSeries)
    mainChart.hideLoading()
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
    swap_norm()
})

$('#zButton').click(function () {

    $('#rawButton').removeClass('active');
    // $('#minMaxButton').removeClass('active');
    $('#zButton').addClass('active');
    if (!normalized) {
        normalized = true;
        swap_norm()
    }
});



