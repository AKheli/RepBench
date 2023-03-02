const CSVzip = (...arr) => Array(Math.max(...arr.map(a => a.length)))
    .fill().map((_, i) => arr.map(a => a[i]).join(",") + "\n");

const addHeader = (Array) => {
    header = originalSeries.map(s => s.series.name).join(",") + "\n"
    Array.unshift(header);
    return Array;
}

const addHeaderSynthetic = (Array) => {
    header = injectedSeries.map(s => s.series.name).join(",") + "\n"
    Array.unshift(header);
    return Array;
}


const exportData = function () {
    let blob = new Blob(addHeader(CSVzip(...originalSeries.map(s => s.originalData))), {type: 'text/csv'});
    let a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = dataTitle + ".csv";
    document.body.appendChild(a);
    a.click();
}

const exportSyntheticData = function () {
    let exportData = injectedSeries.map(s => {
        console.log(s)
        originalData = getOriginalData(s.series.linkedTo)
        return s.originalData.map((v, i) => v !== null ? v : originalData[i])
    })

    let blob = new Blob(addHeaderSynthetic(CSVzip(...exportData), {type: 'text/csv'}));
    let a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = dataTitle + "Synthetic.csv";
    document.body.appendChild(a);
    a.click();
}


// bind exportData to the button with id exportOriginalData
const exportDataBtn = document.getElementById("exportOriginalData")
exportDataBtn.addEventListener("click", exportData)

const exportInjectedDataBtn = document.getElementById("exportInjectedData")
exportInjectedDataBtn.addEventListener("click", exportSyntheticData)


const updateExportInjectedButton = function (injectedSeries) {
    if (injectedSeries === null || injectedSeries.length === 0) {
        console.log(injectedSeries, "AAAA")
        exportInjectedDataBtn.style.display = "none"
    } else {
        exportInjectedDataBtn.style.display = "block"

    }
}
updateExportInjectedButton(injectedSeries)
