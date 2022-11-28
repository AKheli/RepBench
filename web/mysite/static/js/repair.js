let createRepairRequestFormData = function (alg) {
    const form = document.getElementById(alg)
    const repairFormData = new FormData(form)
    repairFormData.append('csrfmiddlewaretoken', csrftoken)
    repairFormData.append("injected_series", JSON.stringify(injectedSeries))
    return repairFormData
}

let repairResult = null
let repair = (alg) => fetch(repair_url, {
    method: 'POST',
    body: createRepairRequestFormData(alg),
}).then(response => response.json()).then(responseJson => {
    repairResult = responseJson
    additionalData = responseJson["additional_repair_info"]
    console.log("additionalData")
    console.log(additionalData)
    if(additionalData){
         if(additionalData["reduced"]){
            add_list_of_data_to_chart(additionalData.reduced, mainchart, "reduced")
        }
    }
    const repSeries = responseJson.repaired_series
    const scores = responseJson.scores
    repairResult = repSeries
    let color = null
    for ( key in repSeries) {
        let repair = repSeries[key]
        let c = addRepairedSeries(repair,color)
        if(color === null) {
            color = c
        }
    }

    // load the score charts html element given all the error metrics
    if (document.getElementById("thatsreallywrong") !== null) {
        document.getElementById("thatsreallywrong").outerHTML = responseJson.html;
    }
    scores["color"] = color
    addScores(scores)

})
