//https://stackoverflow.com/questions/3065342/how-do-i-iterate-through-table-rows-and-cells-in-javascript

const highlightSeries = function (col, row, chart){
    // sets series col and row to be highlighted
    // returns initially highlighted series
    return  chart.series.filter((series,i) => {
        let retval =  series.visible
        console.log(col,i)
        console.log(i==col, "i===col")
        series.setVisible(i==col || i == row)
        return retval
    })
}


const corrTable = document.getElementById("correlation_table");
console.log("setupt corr tabel")
const init_corr_table = function () {
    let i = 0;
    let j = 0;
    for (let row of corrTable.rows) {
        i += 1;
        for (let cell of row.cells) {
            cell.setAttribute("onclick", 'highlightSeries("'+i+'","'+j+'",mainchart)');
        }
        j += 1;
    }
}

init_corr_table()
