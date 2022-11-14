let createInjectFormData = function (form_id) {
    let form = document.getElementById(form_id)
    console.log("Form")
    console.log(form)
    const formData = new FormData(form)
    formData.append('csrfmiddlewaretoken', csrftoken)
    return formData
}

let injectedSeries = {}

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
        series = mainchart.addSeries(s)
        s.data = series.yData
        injectedSeries[s["id"]] = s
        console.log(series.yData)
    })
    return false
}

