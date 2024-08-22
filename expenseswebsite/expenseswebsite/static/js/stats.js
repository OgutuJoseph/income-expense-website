const renderChat=(data, labels) => {
    const ctx = document.getElementById('myChart');

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Last Six Months Expenses',
                    data: data,
                    backgroundColor: [
                      "rgba(255, 99, 132, 0.2)",
                      "rgba(54, 162, 235, 0.2)",
                      "rgba(255, 206, 86, 0.2)",
                      "rgba(75, 192, 192, 0.2)",
                      "rgba(153, 102, 255, 0.2)",
                      "rgba(255, 159, 64, 0.2)",
                    ],
                    borderColor: [
                      "rgba(255, 99, 132, 1)",
                      "rgba(54, 162, 235, 1)",
                      "rgba(255, 206, 86, 1)",
                      "rgba(75, 192, 192, 1)",
                      "rgba(153, 102, 255, 1)",
                      "rgba(255, 159, 64, 1)",
                    ],
                    borderWidth: 1,
                }
            ]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Your Summary'
                }
            }
        }
    });
}

const getChartData = () => {
    fetch('/expense-category-summary')
    .then((res)=>res.json())
    .then((results)=> {
        console.log('chart data results here', results)
        const category_data = results.expense_category_data

        const [labels, data] = [
            Object.keys(category_data),
            Object.values(category_data),
        ];

        // renderChat([], []);
        // renderChat(zenData, labels); |||| Below !! ||||
        renderChat(data, labels);
    });
}

document.onload=getChartData()

