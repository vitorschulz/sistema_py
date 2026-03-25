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

document.addEventListener("click", async function(e){

    const subir = e.target.closest(".subir-shopping")
    const descer = e.target.closest(".descer-shopping")

    if(subir){
        const id = subir.dataset.id
        await fetch(`/shopping/${id}/subir`)
        location.reload()
    }

    if(descer){
        const id = descer.dataset.id
        await fetch(`/shopping/${id}/descer`)
        location.reload()
    }

})

document.addEventListener("click", async function(e){

    const subir = e.target.closest(".subir-loja")
    const descer = e.target.closest(".descer-loja")

    if(subir){
        const id = subir.dataset.id
        await fetch(`/loja/${id}/subir`)
        location.reload()
    }

    if(descer){
        const id = descer.dataset.id
        await fetch(`/loja/${id}/descer`)
        location.reload()
    }

})

document.addEventListener("click", async function(e){

    const btnSubir = e.target.closest(".pedido-acoes .subir")
    const btnDescer = e.target.closest(".pedido-acoes .descer")

    if(btnSubir){

        const id = btnSubir.dataset.id

        await fetch(`/pedidos/${id}/subir`, { method: "POST" })

        const item = btnSubir.closest(".pedido-item")
        const anterior = item.previousElementSibling

        if(anterior && anterior.classList.contains("pedido-item")){
            item.parentNode.insertBefore(item, anterior)
            atualizarOrdem(item.parentNode)
        }

    }

    if(btnDescer){

        const id = btnDescer.dataset.id

        await fetch(`/pedidos/${id}/descer`, { method: "POST" })

        const item = btnDescer.closest(".pedido-item")
        const proximo = item.nextElementSibling

        if(proximo && proximo.classList.contains("pedido-item")){
            item.parentNode.insertBefore(proximo, item)
            atualizarOrdem(item.parentNode)
        }

    }

})

function atualizarOrdem(container){

    const itens = container.querySelectorAll(".pedido-item")

    itens.forEach((item, index) => {

        const numero = item.querySelector(".pedido-ordem")
        numero.textContent = (index + 1) + "."

    })

}

document.addEventListener("click", async function(e){

    const subir = e.target.closest(".cliente-acoes .subir")
    const descer = e.target.closest(".cliente-acoes .descer")

    if(subir){

        const id = subir.dataset.id

        await fetch(`/viagem_cliente/${id}/subir`)

        const item = subir.closest(".cliente-item")
        const anterior = item.previousElementSibling

        if(anterior && anterior.classList.contains("cliente-item")){
            item.parentNode.insertBefore(item, anterior)
            atualizarOrdemClientes(item.parentNode)
        }

    }

    if(descer){

        const id = descer.dataset.id

        await fetch(`/viagem_cliente/${id}/descer`)

        const item = descer.closest(".cliente-item")
        const proximo = item.nextElementSibling

        if(proximo && proximo.classList.contains("cliente-item")){
            item.parentNode.insertBefore(proximo, item)
            atualizarOrdemClientes(item.parentNode)
        }

    }

})

function atualizarOrdemClientes(container){

    const itens = container.querySelectorAll(".cliente-item")

    itens.forEach((item, index) => {

        const numero = item.querySelector("span:first-child")
        numero.textContent = (index + 1) + "."

    })

}

const formFinanceiro = document.getElementById("form-financeiro");

if (formFinanceiro) {

    formFinanceiro.addEventListener("submit", function(e) {
        e.preventDefault();

        const form = e.target;
        const formData = new FormData(form);

        fetch(form.action, {
            method: "POST",
            body: formData
        })
        .then(res => {
            if (!res.ok) throw new Error();
            return res.json();
        })
        .then(data => {

            if (data.erro) {
                alert(data.erro);
                return;
            }

            const lista = document.getElementById("lista-financeiro");
            const acoes = document.createElement("div");
            const btnExcluir = document.createElement("button");

            const item = document.createElement("div");
            item.classList.add("financeiro-item");

            const desc = document.createElement("span");
            desc.classList.add("financeiro-desc");
            desc.textContent = data.descricao || "-";

            const valor = document.createElement("span");
            valor.classList.add("financeiro-valor", data.tipo.toLowerCase());

            const valorFormatado = parseFloat(data.valor).toFixed(2);

            valor.textContent = (data.tipo === "CUSTO" ? "- R$ " : "+ R$ ") + valorFormatado;

            acoes.classList.add("financeiro-acoes");
            btnExcluir.classList.add("btn-excluir");
            btnExcluir.dataset.id = data.id;
            btnExcluir.textContent = "✕";

            acoes.appendChild(valor);
            acoes.appendChild(btnExcluir);

            item.appendChild(desc);
            item.appendChild(acoes);

            lista.appendChild(item);

            atualizarResumo(data.tipo, data.valor);

            form.reset();

            mostrarAlerta("Lançamento adicionado!");
        })
        .catch(() => {
            alert("Erro ao adicionar lançamento");
        });

    });

}

function atualizarResumo(tipo, valor, operacao = "add") {

    const ganhoEl = document.getElementById("total-ganho");
    const custoEl = document.getElementById("total-custo");
    const saldoEl = document.getElementById("saldo");

    let ganho = parseFloat(ganhoEl.textContent);
    let custo = parseFloat(custoEl.textContent);

    valor = parseFloat(valor);

    const fator = operacao === "add" ? 1 : -1;

    if (tipo === "GANHO") {
        ganho += valor * fator;
    } else {
        custo += valor * fator;
    }

    const saldo = ganho - custo;

    ganhoEl.textContent = ganho.toFixed(2);
    custoEl.textContent = custo.toFixed(2);
    saldoEl.textContent = saldo.toFixed(2);
}

document.addEventListener("click", function(e) {

    if (e.target.classList.contains("btn-excluir")) {

        const btn = e.target;
        const id = btn.dataset.id;

        fetch(`/financeiro/${id}/delete`, {
            method: "POST"
        })
        .then(res => res.json())
        .then(data => {

            if (data.erro) {
                alert(data.erro);
                return;
            }

            const item = btn.closest(".financeiro-item");
            item.remove();

            atualizarResumo(data.tipo, parseFloat(data.valor), "remove");

            mostrarAlerta("Lançamento removido!", "error");
        });

    }

});

function mostrarAlerta(mensagem, tipo = "success") {

    let container = document.querySelector(".alerts");

    if (!container) {
        container = document.createElement("div");
        container.classList.add("alerts");
        document.body.appendChild(container);
    }

    const alerta = document.createElement("div");
    alerta.classList.add("alert");

    if (tipo === "error") {
        alerta.classList.add("error");
    }

    alerta.textContent = mensagem;

    container.appendChild(alerta);

    setTimeout(() => {

        alerta.style.transition = "opacity 0.5s ease";
        alerta.style.opacity = "0";

        setTimeout(() => {
            alerta.remove();
        }, 500);

    }, 3000);
}

document.addEventListener("click", function(e){

    const link = e.target.closest(".cliente-link");

    if(link){

        const invalido = link.dataset.invalido === "1";

        if(invalido){
            e.preventDefault();
            mostrarAlerta("Esse pedido está ligado a uma loja ou shopping removido!", "error");
        }

    }

});

document.addEventListener("click", function(e){

    const btn = e.target.closest(".btn-export");

    if(btn){

        const url = btn.dataset.url;
        const mensagem = btn.dataset.alert;

        if(mensagem){
            mostrarAlerta(mensagem);
        }

        // pequeno delay pra deixar o alerta aparecer
        setTimeout(() => {
        }, 150);
    }

});
