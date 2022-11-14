let createBayesianOptFormData = function (form_id) {
    let form = document.getElementById(form_id)
    console.log(form)
    const bayesienOptFormData = new FormData(form)
    bayesienOptFormData.append('csrfmiddlewaretoken', csrftoken)
    bayesienOptFormData.append("injected_series", JSON.stringify(injectedSeries))
    return bayesienOptFormData
}

const opt_container = document.getElementById('optscores-container')
let optchart = Highcharts.chart(opt_container, {
        tooltip: {
            //split: true,
            valueDecimals: 2
        },

        title: {
            text: 'title'
        },




        series: [ { data : [ {name: "a" , y : 2 }, {name: "b" , y : 2 }  , {name: "a" , y : 3 } ]  }]

    });
opt_container.style.display = 'none';
optchart.series[0].remove()

let optimizeCurrentData = (form_id) => fetch(optimization_url, {
    method: 'POST',
    body: createBayesianOptFormData(form_id),
}).then(response => response.json()).then(responseJson => {
    let repair_scores = responseJson.opt_result_series
    let added_series =  optchart.addSeries(repair_scores)
    opt_container.style.display = 'block'; // Show


    let repairedSeries = responseJson.repaired_series
    let counter = 0
    let color = null
    for (key in repairedSeries) {
        let repair = repairedSeries[key]
        s = mainchart.addSeries(repair)
    }
})


