let token = document.currentScript.getAttribute('token');
let fetch_url = document.currentScript.getAttribute('fetchurl')


const chart = Highcharts.chart(document.getElementById('container'), {

    tooltip: {
        formatter: function () {
            // The first returned item is the header, subsequent items are the
            // points
            return ['<b>' + this.x + '</b>'].concat(
                this.points ?
                    this.points.map(function (point) {
                        return point.series.name + ': ' + point.y + 'm';
                    }) : []
            );
        },
        //split: true,
        shared: true,
        valueDecimals: 2
    },


    chart: {
        zoomType: 'x'
    },

    title: {
        text: 'title'
    },

    subtitle: {
        text: 'Using the Boost module'
    },

    accessibility: {
        screenReaderSection: {
            beforeChartFormat: '<{headingTagName}>{chartTitle}</{headingTagName}><div>{chartSubtitle}</div><div>{chartLongdesc}</div><div>{xAxisDescription}</div><div>{yAxisDescription}</div>'
        }
    },


    series: [{data: [1, 2, 3, 4, 5, 6, 7], id: "123"}]

});

const formData = new FormData();
formData.append('csrfmiddlewaretoken', token);

fetch(fetch_url, {
    method: 'post',
    body: formData,
    // headers: {
	// 	'Content-type': 'application/json; charset=UTF-8'
	// }
}).then(response => {

    response.json().then(responseJson => {
        //delete old series
        var seriesLength = chart.series.length;
        for (var i = seriesLength - 1; i > -1; i--) {
            chart.series[i].remove();
        }

        let data = responseJson.series
        console.log("loading data in promise")
        console.log("loading")

        console.log(data)
        data.forEach(x => chart.addSeries(x))
    })

})

// var test_button = document.getElementById("datasetformapply")
// console.log(test_button)
// //test_button.addEventListener("click",
// document.getElementById("datasetform").addEventListener("change",e => {
//     console.log("eventx")
//     let form = document.getElementById("datasetform")
//     const formDatatest = new FormData(form);
//     formDatatest.append('csrfmiddlewaretoken', token);
//     formDatatest.append("set", "set");
//
//     fetch(fetch_url, {
//         method: 'POST',
//         body: formDatatest,
//
//     }).then(response =>
//         response.json().then(responseJson => {
//                 var seriesLength = chart.series.length;
//         for (var i = seriesLength - 1; i > -1; i--) {
//             chart.series[i].remove();
//         }
//
//         let data = responseJson.series
//         console.log("loading data in promise")
//         console.log("loading")
//
//         console.log(data)
//         data.forEach(x => chart.addSeries(x))
//             chart.xAxis[0].setExtremes() // reset the zoom
//             }
//         ))
// })

let createFormData = function(form_id,token){
    let form = document.getElementById(form_id)
    const formData = new FormData(form)
    formData.append('csrfmiddlewaretoken', token)
    formData.append('injected_series', chart.g)
    console.log("FORMDATA")
    console.log(formData)
    return formData
}







let injectedSeries = {}

let createRepairRequestFormData = function(form_id,token){
    console.log(injectedSeries)
    repairformData = createFormData(form_id,token)
    repairformData.append("injected_series" , JSON.stringify(injectedSeries))
    return repairformData
}


let inject  = (form_id, token , fetch_url) =>  fetch(fetch_url, {
        method: 'POST',
        body: createFormData(form_id,token),
    }).then(response =>  response.json()).then(responseJson => {
    //delete old series
    let s = responseJson.series
    let rmse = responseJson.rmse
    if(chart.get(s["id"])){
        chart.get(s["id"]).remove();
    }
    injectedSeries[s["id"]] = s
    chart.addSeries(s)
    document.getElementById("rmse_display").innerHTML = "RMSE :" + responseJson.rmse ;
    })



let repairCurrentData = (form_id, token , fetch_url) =>  fetch(fetch_url, {
        method: 'POST',
        body: createRepairRequestFormData(form_id,token),
    }).then(response =>  response.json()).then(responseJson => {
        console.log(responseJson)
        for(key in responseJson){
            chart.addSeries(responseJson[key])
        }
        document.getElementById("rmse_display").innerHTML = "RMSE :" + responseJson.rmse ;
    })

