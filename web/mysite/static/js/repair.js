let createRepairRequestFormData = function (alg) {
    const form = document.getElementById(alg)
    const repairFormData = new FormData(form)
    repairFormData.append('csrfmiddlewaretoken', csrftoken)

    repairFormData.append("injected_series", JSON.stringify(get_injected_norm_data()))
    return repairFormData
}

let repairResult = null
let repair = (alg) => fetch(repair_url, {
    method: 'POST',
    body: createRepairRequestFormData(alg),
}).then(response => response.json()).then(responseJson => {
    repairResult = responseJson
    additionalData = responseJson["additional_repair_info"]

    if(additionalData){
         if(additionalData["reduced"]){
            add_list_of_data_to_chart(additionalData.reduced, mainChart, "reduced")
        }
    }
    const repSeries = responseJson.repaired_series
    const scores = responseJson.scores
    repairResult = repSeries
    let color = null
    const chartRepairSeries = Object.keys(repSeries).map(key => {
        let repair = repSeries[key]
        let retval = addRepairedSeries(repair,color)
        let c = retval.color
        if(color === null) {
            color = c
        }
        return retval.series
    })



    // load the score charts html element given all the error metrics
    if (document.getElementById("thatsreallywrong") !== null) {
        document.getElementById("thatsreallywrong").outerHTML = responseJson.html;
    }
    scores["color"] = color
    console.log("reptcharSeries", chartRepairSeries)
    addScores(scores,chartRepairSeries)

})
