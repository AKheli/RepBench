let createBayesianOptFormData = function (form_id) {
    let form = document.getElementById(form_id)
    const bayesienOptFormData = new FormData(form)
    bayesienOptFormData.append('csrfmiddlewaretoken', csrftoken)
    bayesienOptFormData.append("injected_series", JSON.stringify(injectedSeries))
    return bayesienOptFormData
}


// const opt_container = document.getElementById('optscores-container')
// let optchart = Highcharts.chart(opt_container, {
//     tooltip: {
//         //split: true,
//         valueDecimals: 2
//     },
//
//     title: {
//         text: 'title'
//     },
//     series: [{data: [{name: "a", y: 2}, {name: "b", y: 2}, {name: "a", y: 3}]}]
//
// });
// opt_container.style.display = 'none';
// optchart.series[0].remove()
//

// function loadTableData(data, error) {
//     $("#myTable tr").remove();
//     $("#testBody tr").remove();
//
//     const table = document.getElementById("myTable");
//     const header = table.createTHead();
//     const row = header.insertRow(0);
//     let header1 = row.insertCell(0);
//     header1.innerHTML = "Iteration";
//
//     let first_col = data[0].name
//     let loss = error
//
//     Object.keys(first_col).forEach((key, i) => {
//         const cell = row.insertCell(i + 1);
//         cell.innerHTML = key;
//     })
//     let cell = row.insertCell(Object.keys(first_col).length + 1)
//     cell.innerHTML = loss;
//     //insert table body
//
//     let body = document.getElementById("testBody");
//     body.innerHTML += "<tr style='border-bottom:1px solid black'> " +
//         "<td colSpan='100%'> Initial Parameters </td> </tr>  "
//     body = document.getElementById("testBody");
//
//
//     data.forEach((item, iter) => {
//             let row = body.insertRow();
//             row.insertCell(0).innerHTML = iter;
//             Object.keys(item.name).forEach((key, i) => {
//                 const cell = row.insertCell(i + 1);
//                 cell.innerHTML = item.name[key];
//             })
//             const cell = row.insertCell(Object.keys(item.name).length + 1);
//             cell.innerHTML = item.y;
//             cell.addstyle = "border-bottom:1px solid black"
//         }
//     )
// }

let optimData = null
let optimizeCurrentData = (form_id) => {
    fetch(optimization_url, {
        method: 'POST',
        body: createBayesianOptFormData(form_id),
    }).then(response => response.json()).then(responseJson => {
        optimData = responseJson
        //textract error_loss from formdata
        let error_loss = optimData.error_loss.toUpperCase();
        let params = Object.keys(optimData.param_ranges);
        let n_initial_points = optimData.n_initial_points;
        let job_id = optimData.job_id;
        initOptChart(params, error_loss)
        fetch_loop(n_initial_points, job_id)
    })


}

let create_job_id_form = function (job_id) {
    const empty_form = new FormData()
    empty_form.append('csrfmiddlewaretoken', csrftoken)
    empty_form.append('job_id', job_id)
    console.log("EMPTY fORM")
    return empty_form
}

function objToString(obj, round) {
    var str = '';
    for (var p in obj) {
        if (Object.prototype.hasOwnProperty.call(obj, p)) {
            str += '<b>' + p + ':</b>  ' + Number(obj[p].toFixed(3)) + '     ';
        }
    }
    return str;
}

let fetch_loop = function (n_initial_points, job_id) {
    console.log("FEEEEEETCH")
    fetch(fetch_opt_result, {
        method: 'POST',
        body: create_job_id_form(job_id),
    }).then(response => response.json()).then(
        responseJson => {
            console.log(responseJson)
            let response_status = responseJson.status
            if (response_status !== "DONE") {
                if (response_status === "running") {
                    let data = responseJson.data
                    optChart.addParamError(Object.values(data.params), data.score)
                }
                fetch_loop(n_initial_points, job_id)
                // setTimeout(function () {
                //     fetch_loop(n_initial_points, job_id)
                // }, 500)
            }

        })



}


