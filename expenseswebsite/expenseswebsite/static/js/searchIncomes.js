const searchField = document.querySelector("#searchField");
const tableOutput = document.querySelector(".table-output");
tableOutput.style.display = "none";
const tableMain = document.querySelector(".table-main");
const paginationContainer = document.querySelector(".pagination-container");
const outputTableBody = document.querySelector(".output-table-body");


searchField.addEventListener("keyup", (e) =>{
    const searchValue = e.target.value;
    console.log("search value: ", searchValue)

    if (searchValue.trim().length > 0){
        paginationContainer.style.display = "none";

        outputTableBody.innerHTML = "";

        fetch("/income/search-incomes", {
            body: JSON.stringify({ searchText: searchValue }),
            method: "POST",
        })
        .then((res) => res.json())
        .then((data) => {
            console.log("data:", data)

            tableMain.style.display = "none";
            tableOutput.style.display = "block";
            if (data.length === 0){
                tableOutput.innerHTML = "No results found."
            } else {
                data.forEach((item)=>{
                    outputTableBody.innerHTML+=`
                        <tr>
                            <td>${ item.amount }</td>
                            <td>${ item.source }</td>
                            <td>${ item.description }</td>
                            <td>${ item.date }</td>
                            <td><a href="{% url 'editIncomesUrl' item.id %}" class="btn btn-info">Edit</a></td>
                        </tr>
                    `
                })                
            }
        });
    } else {        
        tableOutput.style.display = "none";
        tableMain.style.display = "block";
        paginationContainer.style.display = "block";
    }
})