let createBayesianOptFormData = function (form_id) {
    let form = document.getElementById(form_id)
    console.log(form)
    console.log("optimform")

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
    series: [{data: [{name: "a", y: 2}, {name: "b", y: 2}, {name: "a", y: 3}]}]

});
opt_container.style.display = 'none';
optchart.series[0].remove()


function loadTableData(data, error) {
    $("#myTable tr").remove();
    $("#testBody tr").remove();

    const table = document.getElementById("myTable");
    const body = document.getElementById("testBody");
    //insert table header
    const header = table.createTHead();
    const row = header.insertRow(0);
    let header1 = row.insertCell(0);
    header1.innerHTML = "Iteration";

    let first_col = data[0].name
    let loss = error

    Object.keys(first_col).forEach((key, i) => {
        const cell = row.insertCell(i+1);
        cell.innerHTML = key;
    })
    let cell = row.insertCell(Object.keys(first_col).length+1)
    cell.innerHTML = loss;
    //insert table body
    data.forEach((item,iter) => {
            let row = body.insertRow();
            row.insertCell(0).innerHTML = iter;
            Object.keys(item.name).forEach((key, i) => {
                const cell = row.insertCell(i+1);
                cell.innerHTML = item.name[key];
            })
            const cell = row.insertCell(Object.keys(item.name).length+1);
            cell.innerHTML = item.y;
        }
    )
}

let optimData = null
let optimizeCurrentData = (form_id) => fetch(optimization_url, {
    method: 'POST',
    body: createBayesianOptFormData(form_id),
}).then(response => response.json()).then(responseJson => {
    optimData = responseJson
    console.log("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    loadTableData(responseJson.data, responseJson.error_loss)
    // generate table with responseJson.data


    // let repair_scores = responseJson.opt_result_series
    // let added_series =  optchart.addSeries(repair_scores)
    // opt_container.style.display = 'block'; // Show
    // optchart.chart.yAxis[0].axisTitle.attr({
    //     text: 'new title'
    // });
    //
    //
    // let repairedSeries = responseJson.repaired_series
    // let counter = 0
    // let color = null
    // for (key in repairedSeries) {
    //     let repair = repairedSeries[key]
    //     s = mainchart.addSeries(repair)
    // }
})


