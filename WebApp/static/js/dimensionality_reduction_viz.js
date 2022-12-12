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
       return addRepairedSeries(repair,color)
    })
    resetSeries()
    scores["color"] = mainChart.series[mainChart.series.length-2].color
    addScores(scores,chartRepairSeries)

    // const repSeries = responseJson.repaired_series
    // const scores = responseJson.scores
    // repairResult = repSeries
    // let color = null
    // const chartRepairSeries = Object.keys(repSeries).map(key => {
    //     let repair = repSeries[key]
    //     addRepairedSeries(repair, color)
    //
    // })
    //
    //
    // // // load the score charts html element given all the error metrics
    // // if (document.getElementById("thatsreallywrong") !== null) {
    // //     document.getElementById("thatsreallywrong").outerHTML = responseJson.html;
    // // }
    // scores["color"] = mainChart.series[mainChart.series.length - 2].color
    // addScores(scores, chartRepairSeries)

    repairResponse.reductions.forEach((reduction) => {
        reduction.forEach((series) => {
            addReducedSeries(series)
        })
    })


    //lower plot
    const final_reductions = repairResponse.final_reductions
    threshold = final_reductions[0].threshold
    final_reductions.forEach(reduction => {
        reduction.data = reduction.diff_norm
        reduction["yAxis"] = 2
        reduction["lineWidth"] = 2
        reduction["color"] = scores["color"]
        addRepairedSeries(reduction, null)
    })

      const boxes = document.querySelectorAll('.full-height')

    boxes.forEach(box => {
      box.style.height = '110vh';
    });

    resetSeries()

    document.getElementById("after-runtime").innerHTML +=
        "<table class='table'> " +
        "<tr> " +
        "<th> Metric </th> " +
        "<th> Value </th>" +
        "</tr> " +
        "<tr>" +
        "<td>TP</td>" +
        "<td>"+repairResponse.TP+"</td>" +
        "</tr>" +
        "<tr> " +
        "<td>FP</td>" +
        "<td>"+repairResponse.FP+"</td>" +
        "</tr>" +
        "<tr> " +
        "<td>TN</td>" +
        "<td>"+repairResponse.TN+"</td>" +
        "</tr>" +
        "<tr> " +
        "<td>FN</td>" +
        "<td>"+repairResponse.FN+"</td>" +
        "</tr>" +
        "</table>"

    // make highcharts_container higher



})



