// All series that are not part of the orginal graph have to be linked to some other series


function transpose(matrix) {
    console.log(matrix)
  return matrix[0].map((col, i) => matrix.map(row => row[i]));
}


add_list_of_data_to_chart = function (list_of_data, chart,name) {
    console.log("add_list_of_data_to_chart")
    console.log(list_of_data)
    // convert object to array with arrow function
    let data = Object.keys(list_of_data).map(key => list_of_data[key])


    for (let i = 0; i < data.length; i++) {
        if (i > 2 ){
            break
        }
        append_data_to_chart( data[i], chart, name)
    }
}

let originalSeries = null
let options = null
append_data_to_chart = function (data, chart, name) {
    data = transpose(data)
    console.log(data)
    console.log(chart.series)
    console.log("append_data_to_chart")
    originalSeries = chart.series.filter(series => series.linkedSeries.length === 0)
    options = originalSeries[0].options
    //console.assert(data.length === originalSeries.length && data[0].length === originalSeries[0].data.length , "data and chart series must have the same length")

    //iterate throught the charts series with no linked series and add series

    for (let i = 0; i < originalSeries.length; i++) {
        console.log(i)
        let series = chart.series[i]
        id = series.options.id
        console.log("series to add")
        console.log(id)
        chart.addSeries({ data : data[i], name: name+i,  linkedTo: id , color: series.color})
    }

}
