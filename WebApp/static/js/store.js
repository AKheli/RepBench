let createStoreFormData = function () {
    console.log("store")
    const form = document.getElementById("storeForm")
    console.log(form)
    const storeFormData = new FormData(form)
    storeFormData.append('csrfmiddlewaretoken', csrftoken)
    storeFormData.append("injected_series", JSON.stringify(get_injected_norm_data()))
    return storeFormData
}

let store = () => fetch(store_url, {
    method: 'POST',
    body: createStoreFormData(),
}).then(response => response.json()).then(responseJson => {
})

document.getElementById("storeButton").addEventListener('click', store)
