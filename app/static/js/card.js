// Evento disparado quando a página é mostrada (inclusive ao voltar pelo botão do navegador) serve p problemas de cache
window.addEventListener("pageshow", function(event) {
    if (event.persisted) {
        window.location.reload();
    }
});

// Seleciona todos os botões de menu (⋮) dentro dos cards e conmtrola a porra toda
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

// Evento global de clique na página
document.addEventListener("click", function(){

    // Fecha todos os menus quando clicar fora
    document.querySelectorAll(".menu-opcoes").forEach(o=>{
        o.style.display = "none"
    })

    // Remove estado visual de todos os cards
    document.querySelectorAll(".card-viagem").forEach(c=>{
        c.classList.remove("menu-aberto")
    })

})

// Seleciona o formulário de filtro
const formFiltro = document.querySelector(".filtro-viagens form");

if (formFiltro) {

    // Evento disparado ao enviar o formulário
    formFiltro.addEventListener("submit", function(e){

        const inicio = document.getElementById("data_inicio").value;
        const fim = document.getElementById("data_fim").value;

        // Validação: nenhum filtro preenchido
        if(!inicio && !fim && !local){
            e.preventDefault();
            mostrarAlerta("Preencha pelo menos um filtro!", "error");
            return;
        }

        // Validação: data inicial maior que final
        if(inicio && fim && inicio > fim){
            e.preventDefault();

            mostrarAlerta("Data inicial não pode ser maior que a final!", "error");
        }

    });

}

// Cria objeto da URL atual
const url = new URL(window.location.href);

// Pega elemento com dados de filtro vindos do backend
const filtrosEl = document.getElementById("filtros-data");

if (filtrosEl) {
    // Verifica se filtro foi aplicado (string "True" do Flask)
    const filtroAplicado = filtrosEl.dataset.filtrado === "True";
     // Verifica se houve erro de data
    const dataInvalida = filtrosEl.dataset.dataInvalida === "True";

    // Se filtro aplicado, mostra alerta de sucesso
    if (filtroAplicado) {
        mostrarAlerta("Filtro aplicado!", "success");
    }

    // Se data inválida, mostra erro
    if (dataInvalida) {
        mostrarAlerta("Data inválida!", "error");
    }
}

// Verifica se URL contém ?limpo=1
if (url.searchParams.get("limpo") === "1") {
    mostrarAlerta("Filtro limpo!", "success");

    // Remove o parâmetro da URL (sem recarregar a página)
    url.searchParams.delete("limpo");
    // Atualiza a URL no navegador
    window.history.replaceState({}, document.title, url.pathname + url.search);
}


// Função para criar alertas dinâmicos na tela
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