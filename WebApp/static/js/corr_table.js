

function getPointCategoryName(point, dimension) {
            var series = point.series,
                isY = dimension === 'y',
                axis = series[isY ? 'yAxis' : 'xAxis'];
            return axis.categories[point[isY ? 'y' : 'x']];
}

initCorrTable = function(categories, data , id) {
        Highcharts.chart(id, {
            chart: {
                type: 'heatmap',
                marginTop: 40,
                marginBottom: 80,
            },


            title: {
                text: 'Time Series Correlation'
            },

            xAxis: {
                categories: categories
            },

            yAxis: {
                categories: categories,
                reversed: true
            },

            accessibility: {
                point: {
                    descriptionFormatter: function (point) {
                        var ix = point.index + 1,
                            xName = getPointCategoryName(point, 'x'),
                            yName = getPointCategoryName(point, 'y'),
                            val = point.value;
                        return 'Corr between' + xName + 'and' + yName + ':' + val;
                    }
                }
            },

            colorAxis: {
                stops: [
                    [0, Highcharts.getOptions().colors[1]],
                    [0.5, '#FFFFFF'],
                    [1, Highcharts.getOptions().colors[1]]
                ],
                min: -1,
                max: 1,
                minColor: '#FFFFFF',
                maxColor: Highcharts.getOptions().colors[1]

            },

            legend: {
                align: 'right',
                layout: 'vertical',
                margin: 0,
                verticalAlign: 'top',
                y: 25,
                symbolHeight: 280
            },

            tooltip: {
                formatter: function () {
                    return 'Corr(' + getPointCategoryName(this.point, 'x') + ',' +
                        '' + getPointCategoryName(this.point, 'y')
                        + '): <b>' + this.point.value + '</b>';
                }
            },

            series: [{
                name: 'Correlation',
                borderWidth: 0,
                data: corr_data.map(function (point) {
                    return {
                        x: point[0],
                        y: point[1],
                        value: point[2],
                        color: 'rgba(0,0,0,' + point[2] + ')'
                    };
                }),
                dataLabels: {
                    enabled: false,
                    color: '#000000',
                    borderWidth: 0,

                }
            }],

            responsive: {
                rules: [{
                    condition: {
                        maxWidth: 500
                    },
                    chartOptions: {
                        yAxis: {
                            title: {
                                enabled: false
                            },
                            labels: {
                                formatter: function () {
                                    return this.value;
                                }
                            }
                        }
                    }
                }]
            }

        });
}
