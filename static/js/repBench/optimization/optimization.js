let createBayesianOptFormData = function (form_id) {
    var e = document.getElementById("optFormAlgSelect");
    var algorithm = e.value;
    let form = document.getElementById(algorithm)
    let formData = new FormData(form)
    let form_b_opt = document.getElementById("bayesian_opt_form_params")
    const bayesienOptFormData = new FormData(form_b_opt)

    for (var pair of formData.entries()) {
        bayesienOptFormData.append(pair[0], pair[1]);
    }
    console.log("token creation", csrftoken)
    bayesienOptFormData.append('csrfmiddlewaretoken', csrftoken)
    bayesienOptFormData.append("injected_series", JSON.stringify(chartManager.get_injected_norm_data()))
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
        initOptChart(params, error_loss, n_initial_points, n_calls)
        fetch_loop(n_initial_points, job_id)
    })
}

let create_job_id_form = function () {
    const empty_form = new FormData()
    empty_form.append('csrfmiddlewaretoken', csrftoken)
    console.log("EYY")
    console.log(csrftoken)
    console.log("EMPTY fORM", csrftoken)
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
    // Get the CSRF token value from the cookie
    fetch(fetch_opt_result, {
        method: 'POST',
        // headers: {
        //   'Content-Type': 'application/json',
        //   'X-CSRFToken': getCookie('csrftoken')
        // },
        body: create_job_id_form(),
    }).then(response => response.json()).then(
        responseJson => {
            console.log(responseJson)
            let response_status = responseJson.status
            if (response_status !== "DONE") {
                console.log("NOT DONE")
                console.log(response_status)
                if (response_status === "running") {
                    optChart.addParamError(Object.values(responseJson.params), responseJson.score)
                }
                setTimeout(function () {
                    fetch_loop(n_initial_points, job_id)
                }, 1000)
            }
        })
}


