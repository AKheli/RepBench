let createRepairRequestFormData = function (alg) {
    // const form = document.getElementById(alg)
    // const repairFormData = new FormData(form)
    repairFormData.append('csrfmiddlewaretoken', csrftoken)
    // repairFormData.append("injected_series", JSON.stringify(get_injected_norm_data()))
    // return repairFormData
}

let recommendationResults = null

const recommendationFetchPromise = new Promise((resolve, reject) => {
    fetch(recommendation_url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}'
        }
    }).then(response => response.json())
        .then(data => {
            recommendationResults = data

            document.getElementById("rec_info").style.display = "block"
            document.getElementById("used_classifier").innerHTML = "<b>"+ data.used_estimator+"</b>"
            document.getElementById("recommended_algorithm").innerHTML ="<b>"+  data.recommended_algorithm+"</b>"
            createErrorChart(data.alg_score)
            createProbabilityChart(data.probabilities)
            Promise.all([mainChartFetchPromise]).then(() => {
                Object.entries(data.alg_repairs).forEach(([k, v]) => {
                    rep_series = Object.values(v)[0]
                    rep_series.visible = k === data.recommended_algorithm
                    rep_series.legendIndex = k === data.recommended_algorithm ? -2 : -1
                    console.log(rep_series)
                    addRepairedSeries(rep_series, 0)
                });

                resetSeries(true)


            }).catch(error => console.error(error))
        })
})


//
// let repair = (alg) => {
//     createScoreBoard()
//
//     fetch(repair_url, {
//         method: 'POST',
//         body: createRepairRequestFormData(alg),
//     }).then(response => response.json()).then(responseJson => {
//         const repSeries = responseJson.repaired_series
//         const scores = responseJson.scores
//         repairResult = repSeries
//         let color = null
//         repairedSeries.length  = 0
//         const chartRepairSeries = Object.keys(repSeries).map(key => {
//             let repair = repSeries[key]
//             return addRepairedSeries(repair,color)
//         })
//         updateScoreBoard(scores)
//
//         resetSeries(true)
//         scores["color"] = mainChart.series[mainChart.series.length-2].color
//
//
//     })
// }
