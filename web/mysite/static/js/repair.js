let createRepairRequestFormData = function (alg) {
    let form = document.getElementById(alg)
    const repairFormData = new FormData(form)
    repairFormData.append('csrfmiddlewaretoken', csrftoken)
    repairFormData.append("injected_series", JSON.stringify(injectedSeries))
    repairFormData.append("alg_type", alg)

    return repairFormData
}
let repairResult = null
let repair = (alg) => fetch(repair_url, {
    method: 'POST',
    body: createRepairRequestFormData(alg),
}).then(response => response.json()).then(responseJson => {
    repairResult = responseJson
    console.log(repairResult)
    repairedSeries = responseJson.repaired_series
    scores = responseJson.scores

    let counter = 0
    let color = null
    for (key in repairedSeries) {
        let repair = repairedSeries[key]

        if (counter > 0) repair["color"] = color
        s = mainchart.addSeries(repairedSeries[key])
        if (counter === 0) color = s.color
        counter += 1
    }

    // load the score charts html element given all the error metrics
    if (document.getElementById("thatsreallywrong") !== null) {
        document.getElementById("thatsreallywrong").outerHTML = responseJson.html;
    }
    scores["color"] = color
    addScores(scores)


})
