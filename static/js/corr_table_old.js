// const highlightSeries = function (col, row, chart) {
//     const highlighed_before = chart.series.filter((series, scounter) => {
//         let retval = series.visible
//         series.setVisible(scounter == col || scounter == row)
//         return retval
//     })
// }
// let initial_highlighted_series = null;
//
// const reset_series_highlighted = function () {
//     setTimeout(_ => {
//         initial_highlighted_series.forEach(series => series.setVisible(true))
//         initial_highlighted_series = null
//
//     }, 50)
// }
// const set_series_highlighted = function () {
//     if (initial_highlighted_series === null) {
//         initial_highlighted_series = mainChart.series.filter(series => series.visible)
//     }
// }
//
// const corrTable = document.getElementById("correlation_table")
// const corr_div = document.getElementById("correlationMatrix")
//
// corr_div.setAttribute("onmouseleave", 'reset_series_highlighted()')
// corr_div.setAttribute("onmouseover", 'set_series_highlighted()')
//
// const init_corr_table = function () {
//     let r_i = -1;
//     for (let row of corrTable.rows) {
//         let r_j = -1;
//         for (let cell of row.cells) {
//             cell.style.cssText += 'text-align:center;';
//             if (r_i !== -1 || r_j !== -1) {
//                 cell.setAttribute("onclick" +
//                     "", 'highlightSeries("' + r_i + '","' + r_j + '",mainChart)');
//             }
//             r_j += 1;
//         }
//         r_i += 1;
//     }
// }
//
// init_corr_table()
