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

document.querySelectorAll(".subir").forEach(btn => {

    btn.addEventListener("click", async function(){

        const id = this.dataset.id

        await fetch(`/pedidos/${id}/subir`, {
            method: "POST"
        })

        const item = this.closest(".pedido-item")
        const anterior = item.previousElementSibling
        if(anterior && anterior.classList.contains("pedido-item")){
            item.parentNode.insertBefore(item, anterior)
            atualizarOrdem(item.parentNode)
        }

    })

})


document.querySelectorAll(".descer").forEach(btn => {

    btn.addEventListener("click", async function(){

        const id = this.dataset.id

        await fetch(`/pedidos/${id}/descer`, {
            method: "POST"
        })

        const item = this.closest(".pedido-item")
        const proximo = item.nextElementSibling
        if(proximo && proximo.classList.contains("pedido-item")){
            item.parentNode.insertBefore(proximo, item)
            atualizarOrdem(item.parentNode)
        }


    })

})

function atualizarOrdem(container){

    const itens = container.querySelectorAll(".pedido-item")

    itens.forEach((item, index) => {

        const numero = item.querySelector(".pedido-ordem")
        numero.textContent = (index + 1) + "."

    })

}

document.querySelectorAll(".cliente-item .subir").forEach(btn => {

    btn.addEventListener("click", async function(){

        const id = this.dataset.id

        await fetch(`/viagem_cliente/${id}/subir`)

        const item = this.closest(".cliente-item")
        const anterior = item.previousElementSibling

        if(anterior && anterior.classList.contains("cliente-item")){
            item.parentNode.insertBefore(item, anterior)
            atualizarOrdemClientes(item.parentNode)
        }

    })

})

document.querySelectorAll(".cliente-item .descer").forEach(btn => {

    btn.addEventListener("click", async function(){

        const id = this.dataset.id

        await fetch(`/viagem_cliente/${id}/descer`)

        const item = this.closest(".cliente-item")
        const proximo = item.nextElementSibling

        if(proximo && proximo.classList.contains("cliente-item")){
            item.parentNode.insertBefore(proximo, item)
            atualizarOrdemClientes(item.parentNode)
        }

    })

})

function atualizarOrdemClientes(container){

    const itens = container.querySelectorAll(".cliente-item")

    itens.forEach((item, index) => {

        const numero = item.querySelector("span:first-child")
        numero.textContent = (index + 1) + "."

    })

}