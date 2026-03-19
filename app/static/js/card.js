    window.addEventListener("pageshow", function(event) {
    if (event.persisted) {
        window.location.reload();
    }
});


document.querySelectorAll(".menu-card").forEach(menu => {

    menu.addEventListener("click", function(e){

        e.stopPropagation()

        const card = menu.closest(".card-viagem")
        const opcoes = menu.querySelector(".menu-opcoes")

        const aberto = opcoes.style.display === "flex"

        document.querySelectorAll(".menu-opcoes").forEach(o=>{
            o.style.display = "none"
        })

        document.querySelectorAll(".card-viagem").forEach(c=>{
            c.classList.remove("menu-aberto")
        })

        if(!aberto){
            opcoes.style.display = "flex"
            card.classList.add("menu-aberto")
        }

    })

})

document.addEventListener("click", function(){

    document.querySelectorAll(".menu-opcoes").forEach(o=>{
        o.style.display = "none"
    })

    document.querySelectorAll(".card-viagem").forEach(c=>{
        c.classList.remove("menu-aberto")
    })

})

const formFiltro = document.querySelector(".filtro-viagens form");

if (formFiltro) {

    formFiltro.addEventListener("submit", function(e){

        const inicio = document.getElementById("data_inicio").value;
        const fim = document.getElementById("data_fim").value;

        if(!inicio && !fim){
        e.preventDefault();
        mostrarAlerta("Preencha pelo menos uma data!", "error");
        return;
        }

        if(inicio && fim && inicio > fim){
            e.preventDefault();

            mostrarAlerta("Data inicial não pode ser maior que a final!", "error");
        }

    });

}

const url = new URL(window.location.href);

if (url.searchParams.get("filtrado") === "1") {

    mostrarAlerta("Filtro aplicado!", "success");

    url.searchParams.delete("filtrado");
    window.history.replaceState({}, document.title, url.pathname + url.search);

}

if (url.searchParams.get("limpo") === "1") {

    mostrarAlerta("Filtro limpo!", "success");

    url.searchParams.delete("limpo");
    window.history.replaceState({}, document.title, url.pathname + url.search);

}

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