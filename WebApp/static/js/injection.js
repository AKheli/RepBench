let createInjectFormData = function (form_id) {
    let form = document.getElementById(form_id)
    let formData = new FormData(form)
    formData.append('csrfmiddlewaretoken', csrftoken)
    return formData
}

const inject = function () {
    const formData = createInjectFormData('injection_form')
    const columnsToInject = [...formData.getAll('data_columns')]
    formData.forEach((value, key) => {
    })

    const promises = []
    columnsToInject.forEach(val => {
        formData.set('data_columns', val)
        promises.push(
            fetch(injection_url, {
                method: 'POST',
                body: formData,
            }).then(response => response.json()).then(responseJson => {
                //delete old series
                let s = responseJson.injected_series
                //remove old series in the same column
                let previously_injected = null
                if (mainChart.get(s["id"])) {
                    // remove element from injectedSeries list the item with the same id as s["id"]
                    injectedSeries = injectedSeries.filter(inj_s => inj_s.series.id !== s["id"])
                    mainChart.get(s["id"]).remove();
                }
                s["dashStyle"] = 'ShortDot'
                addInjectedSeries(s, previously_injected)
            })
        )

    })
    Promise.all(promises).then(() => {
        resetSeries()
    })
    return false
}

