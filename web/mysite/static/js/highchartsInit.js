let chart = null
fetchChart = function (token, fetch_url) {
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
            data.forEach(x => chart.addSeries(x))
        })

    })
}

let createFormData = function (form_id, token) {
    let form = document.getElementById(form_id)
    console.log("Form")

    console.log(form)

    const formData = new FormData(form)
    formData.append('csrfmiddlewaretoken', token)
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

        if (counter > 0) repair["color"] = color
        s = chart.addSeries(repairedSeries[key])
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


let createOptimizeRequestFormData = function (form_id, token) {
    repairformData = createFormData(form_id, token)
    repairformData.append("injected_series", JSON.stringify(injectedSeries))
    let form = document.getElementById(form_id)
    const children = Array.from(form.children);

    dict = {}
    children.forEach(child => {
        console.log(child.id)
        if (child.id) {
            if (child.id in dict) {
                dict[child.id].push(child.value)
            } else {
                dict[child.id] = [child.value]
            }
        }
        repairformData.append("param_ranges", JSON.stringify(dict))
    })
    return repairformData
}



const opt_container = document.getElementById('container-optscores')
let optchart = Highcharts.chart(opt_container, {
        tooltip: {
            //split: true,
            valueDecimals: 2
        },

        title: {
            text: 'title'
        },


        accessibility: {
            screenReaderSection: {
                beforeChartFormat: '<{headingTagName}>AAAAAAAAAAA{chartTitle}</{headingTagName}><div>{chartSubtitle}</div><div>{chartLongdesc}</div><div>{xAxisDescription}</div><div>{yAxisDescription}</div>'
            }
        },


        series: [ { data : [ {name: "a" , y : 2 }, {name: "b" , y : 2 }  , {name: "a" , y : 3 } ]  }]

    });
opt_container.style.display = 'none';
optchart.series[0].remove()

let optimizeCurrentData = (form_id, token, fetch_url) => fetch(fetch_url, {
    method: 'POST',
    body: createOptimizeRequestFormData(form_id, token),
}).then(response => response.json()).then(responseJson => {
    let repair_res = responseJson.opt_result_series
    let added_series =  optchart.addSeries(repair_res)
    opt_container.style.display = 'block';          // Show
})



