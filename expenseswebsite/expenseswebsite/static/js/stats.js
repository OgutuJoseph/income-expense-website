const renderChat=(zenData, zenLabels) => {
    const ctx = document.getElementById('myChart');

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: zenLabels,
            datasets: [
                {
                    label: 'Last Six Months Expenses',
                    data: zenData,
                    borderWidth: 1
                }
            ]
        },
        options: {
            // scales: {
            //     y: {
            //         beginAtZero: true
            //     }
            // }
            plugins: {
                title: {
                    display: true,
                    text: 'Your Summary'
                }
            }
        }
    });
}

const getChartData = () =>

document.onload=getChartData

