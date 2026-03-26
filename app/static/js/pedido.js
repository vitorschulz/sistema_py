const shopping = document.getElementById("shopping")
const loja = document.getElementById("loja")

document.addEventListener("DOMContentLoaded", function(){

    const form = document.querySelector("form");

    if(!form) return;

    form.addEventListener("submit", function(e){

        const checkboxes = form.querySelectorAll('input[name="tipo[]"]');
        const algumMarcado = Array.from(checkboxes).some(cb => cb.checked);

        if(!algumMarcado){
            e.preventDefault();
            mostrarAlerta("Selecione pelo menos um tipo!", "error");
        }

    });

});

function filtrarLojas(){

    const shoppingId = shopping.value

    for(let option of loja.options){

        const lojaShopping = option.dataset.shopping

        option.style.display =
            lojaShopping == shoppingId ? "block" : "none"

    }

}


shopping.addEventListener("change", () => {

    loja.value = ""
    filtrarLojas()

})


filtrarLojas()

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