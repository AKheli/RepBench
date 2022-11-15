// let chart = null
// fetchChart = function (token, fetch_url) {
//     const formData = new FormData();
//     formData.append('csrfmiddlewaretoken', token);
//     chart = initMainChart()
//
//     fetch(fetch_url, {
//         method: 'post',
//         body: formData,
//         // headers: {
//         // 	'Content-type': 'application/json; charset=UTF-8'
//         // }
//     }).then(response => {
//         response.json().then(responseJson => {
//             //delete old series
//             var seriesLength = chart.series.length;
//             for (var i = seriesLength - 1; i > -1; i--) {
//                 chart.series[i].remove();
//             }
//             let data = responseJson.series
//             data.forEach(x => chart.addSeries(x))
//         })
//
//     })
// }
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
