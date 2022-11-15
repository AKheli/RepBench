//
//
// let  initMainChart = function(initial_series = {data:[0]}){
//     const mainchart = Highcharts.chart(document.getElementById('container'), {
//
//         tooltip: {
//
//             formatter: function (e) {
//                 // The first returned item is the header, subsequent items are the
//                 // points
//                 let x = this.x
//                 return ['<p style=\"color:black;font-size:15px;\"> Truth: '  + this.y + '</p>'].concat(
//                     this.series.linkedSeries.map(function (s) {
//                         selectedY = s.yData[x]
//                         if (selectedY !== null) {
//                             selectedY = Math.round(selectedY* 1000) / 1000
//                             if (s.name.includes('injected')){
//                                 return "<br> <p style=\"color:red;font-size:15px;\"> Anomalous: " + selectedY +"<\p> "
//                             } else return "<br> <p style=\"color:"+s.color+";font-size:15px;\">" + s.name +": "+ selectedY +"<\p> "
//                         } else return ""
//                     })
//                 );
//             },
//             //split: true,
//             shared: false,
//             valueDecimals: 2
//         },
//
//
//         chart: {
//             zoomType: 'x'
//         },
//
//         title: {
//             text: 'title'
//         },
//
//
//         accessibility: {
//             screenReaderSection: {
//                 beforeChartFormat: '<{headingTagName}>{chartTitle}</{headingTagName}><div>{chartSubtitle}</div><div>{chartLongdesc}</div><div>{xAxisDescription}</div><div>{yAxisDescription}</div>'
//             }
//         },
//
//
//         series: [initial_series]
//
//     });
//     return mainchart
// }
