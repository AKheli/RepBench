

let chart = null
fetchChart = function(token, fetch_url) {
    const formData = new FormData();
    formData.append('csrfmiddlewaretoken', token);
    chart = initMainChart()

    fetch(fetch_url, {
        method: 'post',
        body: formData,
        // headers: {
        // 	'Content-type': 'application/json; charset=UTF-8'
        // }
    }).then(response => {
        response.json().then(responseJson => {
            //delete old series
            var seriesLength = chart.series.length;
            for (var i = seriesLength - 1; i > -1; i--) {
                chart.series[i].remove();
            }

            let data = responseJson.series
            console.log("loading data in promise")
            console.log("loading")

            console.log(data)
            data.forEach(x => chart.addSeries(x))
        })

    })
}
// var test_button = document.getElementById("datasetformapply")
// console.log(test_button)
// //test_button.addEventListener("click",
// document.getElementById("datasetform").addEventListener("change",e => {
//     console.log("eventx")
//     let form = document.getElementById("datasetform")
//     const formDatatest = new FormData(form);
//     formDatatest.append('csrfmiddlewaretoken', token);
//     formDatatest.append("set", "set");
//
//     fetch(fetch_url, {
//         method: 'POST',
//         body: formDatatest,
//
//     }).then(response =>
//         response.json().then(responseJson => {
//                 var seriesLength = chart.series.length;
//         for (var i = seriesLength - 1; i > -1; i--) {
//             chart.series[i].remove();
//         }
//
//         let data = responseJson.series
//         console.log("loading data in promise")
//         console.log("loading")
//
//         console.log(data)
//         data.forEach(x => chart.addSeries(x))
//             chart.xAxis[0].setExtremes() // reset the zoom
//             }
//         ))
// })

let createFormData = function (form_id, token) {
    let form = document.getElementById(form_id)
    console.log(form)
    const formData = new FormData(form)
    formData.append('csrfmiddlewaretoken', token)
    formData.append('injected_series', chart.g)
    console.log("FORMDATA")
    console.log(formData)
    return formData
}


let injectedSeries = {}

let createRepairRequestFormData = function (form_id, token) {
    console.log(injectedSeries)
    repairformData = createFormData(form_id, token)
    repairformData.append("injected_series", JSON.stringify(injectedSeries))
    return repairformData
}


let inject = (form_id, token, fetch_url) => fetch(fetch_url, {
    method: 'POST',
    body: createFormData(form_id, token),
}).then(response => response.json()).then(responseJson => {
    //delete old series
    let s = responseJson.series
    let rmse = responseJson.rmse
    if (chart.get(s["id"])) {
        chart.get(s["id"]).remove();
    }
    s["dashStyle"] = 'ShortDot'
    series = chart.addSeries(s)
    s.data = series.yData
    injectedSeries[s["id"]] = s
    console.log(series.yData)
})


let repairCurrentData = (form_id, token, fetch_url) => fetch(fetch_url, {
    method: 'POST',
    body: createRepairRequestFormData(form_id, token),
}).then(response => response.json()).then(responseJson => {
    repairedSeries = responseJson.repaired_series
    scores = responseJson.scores


    let counter = 0
    let color = null
    for (key in repairedSeries) {
        let repair = repairedSeries[key]

        if(counter > 0) repair["color"] = color
        s = chart.addSeries(repairedSeries[key])
        if(counter === 0) color = s.color
        counter += 1
    }

    // load the score charts html element given all the error metrics
    if (document.getElementById("thatsreallywrong") !== null) {
        document.getElementById("thatsreallywrong").outerHTML = responseJson.html;
    }
    scores["color"] = color
    addScores(scores)


})



