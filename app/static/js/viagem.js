const select = document.getElementById("status-select")
const viagemId = select.dataset.viagemId

select.addEventListener("change", function(){

    fetch(`/viagens/${viagemId}/status`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            status: select.value
        })
    })
    .then(response => response.json())
    .then(data => {
    })

})