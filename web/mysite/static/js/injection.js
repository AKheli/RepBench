let createInjectFormData = function (form_id) {
    let form = document.getElementById(form_id)
    const formData = new FormData(form)
    formData.append('csrfmiddlewaretoken', csrftoken)
    return formData
}

const inject = function () {
    fetch(injection_url, {
        method: 'POST',
        body: createInjectFormData("injection_form"),
    }).then(response => response.json()).then(responseJson => {
        //delete old series
        let s = responseJson.injected_series
        if (mainChart.get(s["id"])) {
            const to_remove = injectedSeries.map((inj_s, i) => {
                return inj_s.chartSeries.options.id === s["id"] ? i : -1
            }).filter(ind => ind > -1)
            to_remove.forEach(ind => injectedSeries.splice(ind, 1))
            mainChart.get(s["id"]).remove();

        }
        s["dashStyle"] = 'ShortDot'
        addInjectedSeries(s)
    })
    return false
}

