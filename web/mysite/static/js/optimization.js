let createBayesianOptFormData = function (form_id) {
    let form = document.getElementById(form_id)
    const bayesienOptFormData = new FormData(form)
    bayesienOptFormData.append('csrfmiddlewaretoken', csrftoken)
    bayesienOptFormData.append("injected_series", JSON.stringify(get_injected_norm_data()))
    return bayesienOptFormData
}


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
        let n_calls = optimData.n_calls;
        let job_id = optimData.job_id;
        console.log("OPTFETCH")
        initOptChart(params, error_loss, n_initial_points, n_calls)
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
    console.log("START FETCH")
    fetch(fetch_opt_result, {
        method: 'POST',
        body: create_job_id_form(job_id),
    }).then(response => response.json()).then(
        responseJson => {
            console.log(responseJson)
            let response_status = responseJson.status
            if (response_status !== "DONE") {
                console.log("NOT DONE")
                if (response_status === "running") {
                    optChart.addParamError(Object.values(responseJson.params), responseJson.score)
                }
                setTimeout(function () {
                    fetch_loop(n_initial_points, job_id)
                }, 1000)
            }

        })



}


