const CSVzip = (...arr) => Array(Math.max(...arr.map(a => a.length)))
    .fill().map((_, i) => arr.map(a => a[i]).join(",") + "\n");

const addHeader = (Array) => {
    header = originalSeries.map(s => s.series.name).join(",") + "\n"
    Array.unshift(header);
    return Array;
}

const exportData = function () {
    console.log("exporting original series")
    let blob = new Blob(addHeader(CSVzip(...originalSeries.map(s => s.originalData))), {type: 'text/csv'});
    let a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'myFile.csv';
    document.body.appendChild(a);
    a.click();
}

const exportSyntheticData = function () {
    console.log(injectedSeries.map(s => s.originalData))
    console.log("exporting injected series")
    let blob = new Blob(addHeader(CSVzip(...injectedSeries.map(s => s.originalData))), {type: 'text/csv'});
    let a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'myFile.csv';
    document.body.appendChild(a);
    a.click();
}


// bind exportData to the button with id exportOriginalData
const exportDataBtn = document.getElementById("exportOriginalData")
exportDataBtn.addEventListener("click", exportData)

//todo check order of creation of synthetic series
const exportInjectedDataBtn = document.getElementById("exportInjectedData")
exportInjectedDataBtn.addEventListener("click", exportSyntheticData)

const updateExportInjectedButton = function (injectedSeries) {
    if (injectedSeries === null || injectedSeries.length === 0) {
        console.log(injectedSeries, "AAAA")
        exportInjectedDataBtn.style.display = "none"
    }
    else {
        exportInjectedDataBtn.style.display = "block"

    }
}
updateExportInjectedButton(injectedSeries)
