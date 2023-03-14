let createStoreFormData = function (selectionOnly = false) {
    console.log("store")
    const form = document.getElementById("storeForm")
    console.log(form)
    const storeFormData = new FormData(form)
    storeFormData.append('csrfmiddlewaretoken', csrftoken)
    storeFormData.append("injected_series", JSON.stringify(get_injected_norm_data()))

    let { min, max } = mainChart.series[0].xAxis.getExtremes();
    let visible = originalSeries.filter(s => s.chartSeries.visible).map(s => s.name)
    storeFormData.append("min", min)
    storeFormData.append("max", max)
    storeFormData.append("visible_series", JSON.stringify(visible))
    storeFormData.append("selectionOnly",selectionOnly)

    return storeFormData
}

let store = (selectionOnly=false) => fetch(store_url, {
    method: 'POST',
    body: createStoreFormData(selectionOnly),
}).then(response => response.json()).then(responseJson => {
})

document.getElementById("storeButton").addEventListener('click', store)
document.getElementById("storeSelectionButton").addEventListener('click', () => store(true)   )
