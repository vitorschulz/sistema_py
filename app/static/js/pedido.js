// Select de shopping (usado para filtrar lojas)
const shopping = document.getElementById("shopping")
// Select de lojas (vai ser filtrado dinamicamente)
const loja = document.getElementById("loja")
// Pega o local da viagem
const viagemLocal = document.getElementById("viagem-local")?.value

// Filtra shoppings pelo local da viagem
function filtrarShoppings() {
    let primeiraSelecionavel = null

    for (let option of shopping.options) {
        if (option.value === "") continue // mantém placeholder

        const pertence = option.dataset.local === viagemLocal
        option.hidden = !pertence
        option.disabled = !pertence

        if (pertence && !primeiraSelecionavel) {
            primeiraSelecionavel = option
        }
    }

    // Se a opção atual não é do local, reseta
    const optionAtual = shopping.options[shopping.selectedIndex]
    if (optionAtual && optionAtual.disabled) {
        shopping.value = ""
        filtrarLojas()
    }
}

document.addEventListener("DOMContentLoaded", function(){

    const form = document.querySelector("form");

    // Se não existir form, para execução (evita erro global)
    if(!form) return;

    if (viagemLocal) filtrarShoppings()

    form.addEventListener("submit", function(e){

        const btn = form.querySelector("button[type='submit']");

        // Evita múltiplos cliques no botão
        if (btn && btn.dataset.clicked) {
            e.preventDefault();
            return;
        }

        const ehAnotacao = form.hasAttribute('data-anotacao');

        // pelo menos um checkbox deve estar marcado
        const checkboxes = form.querySelectorAll('input[name="tipo[]"]');
        const algumMarcado = Array.from(checkboxes).some(cb => cb.checked);

        if(!algumMarcado && !ehAnotacao){
            e.preventDefault();
            // Mostra alerta visual
            mostrarAlerta("Selecione pelo menos um tipo!", "error");
            return;
        }

        // Só desativa botão depois de tudo válido
        if (btn) {
            btn.dataset.clicked = "true";
            btn.disabled = true;
            btn.innerText = "Salvando...";
        }

    });

});

// filtra loja por shop
function filtrarLojas(){

    const shoppingId = shopping.value

    // Percorre todas as opções de loja
    for(let option of loja.options){

        // Pega o shopping relacionado à loja (data attribute)
        const lojaShopping = option.dataset.shopping

        option.style.display =
            lojaShopping == shoppingId ? "block" : "none"

    }

}

// qnd troca shop
shopping.addEventListener("change", () => {
    // reseta e atualiza lista filtrada
    loja.value = ""
    filtrarLojas()

})

filtrarLojas()

// alerta custom
function mostrarAlerta(mensagem, tipo = "success") {

    // Procura container de alertas
    let container = document.querySelector(".alerts");

    // Cria alerta
    if (!container) {
        container = document.createElement("div");
        container.classList.add("alerts");
        document.body.appendChild(container);
    }

    // Cria alerta
    const alerta = document.createElement("div");
    alerta.classList.add("alert");

    // Adiciona classe de erro se necessário
    if (tipo === "error") {
        alerta.classList.add("error");
    }

    // Define mensagem
    alerta.textContent = mensagem;

    // Adiciona no container
    container.appendChild(alerta);

    // Remove automaticamente após 3s
    setTimeout(() => {

        alerta.style.transition = "opacity 0.5s ease";
        alerta.style.opacity = "0";

        setTimeout(() => {
            alerta.remove();
        }, 500);

    }, 3000);
}