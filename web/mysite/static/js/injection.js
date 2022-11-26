
let createInjectFormData = function (form_id) {
    let form = document.getElementById(form_id)
    const formData = new FormData(form)
    formData.append('csrfmiddlewaretoken', csrftoken)
    return formData
}

const inject = function() {
    fetch(injection_url , {
        method: 'POST',
        body: createInjectFormData("injection_form"),
    }).then(response => response.json()).then(responseJson => {
        //delete old series
        let s = responseJson.series
        if (mainchart.get(s["id"])) {
            mainchart.get(s["id"]).remove();
        }
        s["dashStyle"] = 'ShortDot'
        addInjectedSeries(s)
    })
    return false
}

