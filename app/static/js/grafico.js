// Executa quando o DOM estiver carregado
document.addEventListener("DOMContentLoaded", function () {

    // ===== GRÁFICO =====
    // Lê os dados vindos do backend (JSON embutido no HTML)
    const dados = JSON.parse(
        document.getElementById("dados-grafico").textContent
    );

    const ctx = document.getElementById('graficoFinanceiro');

    // Cria gráfico de linhas com receitas, custos e lucros
    new Chart(ctx, {
        type: "line",
        data: {
            labels: dados.labels,
            datasets: [
                { label: "Receita", data: dados.receitas, borderColor: "green" },
                { label: "Custo", data: dados.custos, borderColor: "red" },
                { label: "Lucro", data: dados.lucros, borderColor: "blue" }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });

    // ===== FILTRO =====
    const form = document.querySelector(".filtro-viagens form");

    if (form) {
        form.addEventListener("submit", function(e){

            const inicio = document.getElementById("data_inicio").value;
            const fim = document.getElementById("data_fim").value;

            if (!validarFiltroData(inicio, fim)) {
                e.preventDefault();
            }

        });
    }

    // ===== ALERTAS =====
    verificarAlertasURL();

});
// Exibe alertas dinâmicos na tela (sem usar Flask flash)
function mostrarAlerta(mensagem, tipo = "success") {

    let container = document.querySelector(".alerts");
    // Cria container se não existir
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
    // Remove automaticamente após 3s
    setTimeout(() => {
        alerta.style.transition = "opacity 0.5s ease";
        alerta.style.opacity = "0";

        setTimeout(() => {
            alerta.remove();
        }, 500);
    }, 3000);
}


// Valida datas do filtro antes de enviar o form
function validarFiltroData(inicio, fim) {
    // Nenhuma data preenchida
    if (!inicio && !fim) {
        mostrarAlerta("Preencha pelo menos uma data!", "error");
        return false;
    }
    // Data inicial maior que final
    if (inicio && fim && inicio > fim) {
        mostrarAlerta("Data inicial não pode ser maior que a final!", "error");
        return false;
    }

    return true;
}


// Exibe alertas com base em parâmetros da URL (?filtrado=1, ?limpo=1)
function verificarAlertasURL() {

    const url = new URL(window.location.href);

    if (url.searchParams.get("filtrado") === "1") {

        mostrarAlerta("Filtro aplicado!", "success");
        // Remove parâmetro da URL sem recarregar
        url.searchParams.delete("filtrado");
        window.history.replaceState({}, document.title, url.pathname + url.search);
    }

    if (url.searchParams.get("limpo") === "1") {

        mostrarAlerta("Filtro limpo!", "success");

        url.searchParams.delete("limpo");
        window.history.replaceState({}, document.title, url.pathname + url.search);
    }

}
