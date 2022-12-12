let createInjectFormData = function (form_id) {
    let form = document.getElementById(form_id)
    const formData = new FormData(form)
    formData.append('csrfmiddlewaretoken', csrftoken)
    return formData
}

const inject = function () {
    const formData = createInjectFormData('injection_form')
    const columnsToInject = [...formData.getAll('data_columns')]
    formData.forEach((value, key) => {
        console.log(key, value)
    })

    columnsToInject.forEach(val => {
        formData.set('data_columns', val)

        fetch(injection_url, {
            method: 'POST',
            body: formData,
        }).then(response => response.json()).then(responseJson => {
            //delete old series
            let s = responseJson.injected_series
            //remove old series in the same column
            let previously_injected = null
            if (mainChart.get(s["id"])) {
                const list_with_one_element = injectedSeries.filter(inj_s => inj_s.series.id === s["id"])
                console.log("list_with_one_element", list_with_one_element)
                previously_injected = list_with_one_element[0]
                const to_remove = injectedSeries.map((inj_s, i) => {
                    return inj_s.chartSeries.options.id === s["id"] ? i : -1
                }).filter(ind => ind > -1)
                to_remove.forEach(ind => injectedSeries.splice(ind, 1))
                mainChart.get(s["id"]).remove();
            }

            s["dashStyle"] = 'ShortDot'
            console.log(previously_injected)
            addInjectedSeries(s, previously_injected)
            resetSeries()

        })
    })
    return false
}

