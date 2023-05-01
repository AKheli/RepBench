$('#rawButton').click(function () {
    $('#zButton').removeClass('active');
    // $('#minMaxButton').removeClass('active');
    $('#rawButton').addClass('active');
    chartManager.normalized = false;
    chartManager.resetSeries()
})

$('#zButton').click(function () {
    $('#rawButton').removeClass('active');
    // $('#minMaxButton').removeClass('active');
    $('#zButton').addClass('active');
    if (!chartManager.normalized ) {
        chartManager.normalized = true;
        chartManager.resetSeries()
    }
});