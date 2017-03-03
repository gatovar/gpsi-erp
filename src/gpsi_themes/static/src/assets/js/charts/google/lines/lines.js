/* ------------------------------------------------------------------------------
 *
 *  # Google Visualization - lines
 *
 *  Google Visualization line chart demonstration
 *
 *  Version: 1.0
 *  Latest update: August 1, 2015
 *
 * ---------------------------------------------------------------------------- */


// Line chart
// ------------------------------

// Initialize chart
google.load("visualization", "1", {packages:["corechart"]});
google.setOnLoadCallback(onDrawLineChart);


function onDrawLineChart() {
    drawComplaintsLineChart();
    drawLineChart();
    drawVendorAuditEfficiencyLineChart();
}

// Chart settings
function drawLineChart() {

    // Data
    var data = google.visualization.arrayToDataTable([
        ['Year', 'Documentation', 'Packaging', 'Distribution'],
        ['01/2004',  90,              80,          95],
        ['06/2004',  95,              60,          80],
        ['02/2005',  80,              90,          100],
        ['06/2005',  100,             90,          90],
        ['01/2006',  60,              70,          80],
        ['06/2006',  65,             65,          85]
    ]);

    // Options
    var options = {
        fontName: 'Roboto',
        height: 400,
        curveType: 'function',
        fontSize: 12,
        chartArea: {
            left: '5%',
            width: '90%',
            height: 350
        },
        pointSize: 4,
        tooltip: {
            textStyle: {
                fontName: 'Roboto',
                fontSize: 13
            }
        },
        vAxis: {
            title: 'Efficiency',
            titleTextStyle: {
                fontSize: 13,
                italic: false
            },
            gridlines:{
                color: '#e5e5e5',
                count: 10
            },
            minValue: 0
        },
        legend: {
            position: 'top',
            alignment: 'center',
            textStyle: {
                fontSize: 12
            }
        }
    };

    // Draw chart
    if ($('#google-line').length) {
        var line_chart = new google.visualization.LineChart($('#google-line')[0]);
        line_chart.draw(data, options);
    }
}

function drawVendorAuditEfficiencyLineChart() {

    // Data
    var data = google.visualization.arrayToDataTable([
        ['Year', 'Documentation', 'Packaging', 'Distribution'],
        ['01/2004',  80,              40,          95],
        ['06/2004',  34,              55,          92],
        ['02/2005',  78,              60,          86],
        ['06/2005',  92,             75,          84],
        ['01/2006',  96,              72,          74],
        ['06/2006',  78,             86,          72]
    ]);

    // Options
    var options = {
        fontName: 'Roboto',
        height: 400,
        curveType: 'function',
        fontSize: 12,
        chartArea: {
            left: '5%',
            width: '90%',
            height: 350
        },
        pointSize: 4,
        tooltip: {
            textStyle: {
                fontName: 'Roboto',
                fontSize: 13
            }
        },
        vAxis: {
            title: 'Efficiency',
            titleTextStyle: {
                fontSize: 13,
                italic: false
            },
            gridlines:{
                color: '#e5e5e5',
                count: 10
            },
            minValue: 0
        },
        legend: {
            position: 'top',
            alignment: 'center',
            textStyle: {
                fontSize: 12
            }
        }
    };

    // Draw chart
    if ($('#va-report-line').length) {
        var line_chart = new google.visualization.LineChart($('#va-report-line')[0]);
        line_chart.draw(data, options);
    }
}

function drawComplaintsLineChart() {

    // Data
    var data = google.visualization.arrayToDataTable([
        ['Day', 'Current', 'Previous'],
        ['Sept 1',  90,              80],
        ['Sept 2',  95,              60],
        ['Sept 3',  80,              70],
        ['Sept 4',  100,             70],
        ['Sept 5',  60,              45],
        ['Sept 6',  65,              60]
    ]);

    // Options
    var options = {
        fontName: 'Roboto',
        height: 400,
        curveType: 'function',
        fontSize: 12,
        chartArea: {
            left: '5%',
            width: '90%',
            height: 350
        },
        pointSize: 4,
        tooltip: {
            textStyle: {
                fontName: 'Roboto',
                fontSize: 13
            }
        },
        vAxis: {
            title: '# Complaints',
            titleTextStyle: {
                fontSize: 13,
                italic: false
            },
            gridlines:{
                color: '#e5e5e5',
                count: 10
            },
            minValue: 0
        },
        legend: {
            position: 'top',
            alignment: 'center',
            textStyle: {
                fontSize: 12
            }
        }
    };

    // Draw chart
    if ($('#complaints-line').length) {
        var line_chart = new google.visualization.LineChart($('#complaints-line')[0]);
        line_chart.draw(data, options);
    }
}


// Resize chart
// ------------------------------

$(function () {

    // Resize chart on sidebar width change and window resize
    $(window).on('resize', resize);
    $(".sidebar-control").on('click', resize);

    // Resize function
    function resize() {
        drawComplaintsLineChart();
        drawLineChart();
        drawVendorAuditEfficiencyLineChart();
    }
});
