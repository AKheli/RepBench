let repairResult = null
let repairResponse = null
let createRepairRequestFormData = function (alg) {
    const form = document.getElementById(alg)
    const repairFormData = new FormData(form)
    repairFormData.append('csrfmiddlewaretoken', csrftoken)

    repairFormData.append("injected_series", JSON.stringify(get_injected_norm_data()))
    return repairFormData
}


let repair = (alg) => fetch(repair_url, {
    method: 'POST',
    body: createRepairRequestFormData(alg),
}).then(response => response.json()).then(responseJson => {
    repairResponse = responseJson
    const repSeries = responseJson.repaired_series
    const scores = responseJson.scores
    repairResult = repSeries
    let color = null
    const chartRepairSeries = Object.keys(repSeries).map(key => {
        let repair = repSeries[key]
        let retval = addRepairedSeries(repair, color)
        let c = retval.color
        if (color === null) {
            color = c
        }
        return retval.series
    })


    // load the score charts html element given all the error metrics
    if (document.getElementById("thatsreallywrong") !== null) {
        document.getElementById("thatsreallywrong").outerHTML = responseJson.html;
    }
    scores["color"] = color
    addScores(scores, chartRepairSeries)
    repairResponse.reductions.forEach((reduction) => {
        reduction.forEach((series) => {
            addReducedSeries(series)
        })
    })
    mainChart.redraw()


    //lower plot
    const final_reductions = repairResponse.final_reductions
    splitMainChart(final_reductions[0].threshold)

    final_reductions.forEach(reduction => {
        reduction.data = reduction.diff_norm
        reduction["yAxis"] = 1
        reduction["lineWidth"] = 2
        mainChart.addSeries(reduction)
    })

})


let splitMainChart = function (treshold) {
    mainChart.update({
        yAxis: [{
            title: {
                text: 'Parameters'
            },
            height: '53%',
            lineWidth: 2,
        }, {
            title: {
                text: "Normalized Difference"
            },
            top: '57%',
            height: '43%',
            offset: 0,
            lineWidth: 2,
            min: -1,
            max: 10,
        }], Series: mainChart.series.concat([{
            //error chart
            showInLegend: false,
            type: 'line',
            color: 'red',
            data: [1, 3, 4, 5, 6, 7],
            yAxis: 1,
        }]),

    })

    mainChart.yAxis[1].addPlotLine(
        {
            color: '#FF0000',
            width: 1,
            style:"dash",
            value: treshold ,
            yAxis: 1,
             label: {
                text: 'Threshold',
                align: 'right',
                x: -10
            }
        }
    )
}
