// Datas das viagens vindas do backend (JSON no HTML)
const datasViagens = JSON.parse(
    document.getElementById("datas-viagens").textContent
)

// Data atual usada como base do calendário
let dataAtual = new Date()

// Gera o calendário do mês atual
function gerarCalendario() {
    const ano = dataAtual.getFullYear()
    const mes = dataAtual.getMonth()

    // Último dia do mês
    const ultimoDia = new Date(ano, mes + 1, 0)

    const calendario = document.getElementById("calendario")
    calendario.innerHTML = ""

    // Atualiza título (ex: Março de 2026)
    atualizarTitulo(ano, mes)

    // Cria os dias do mês
    for (let dia = 1; dia <= ultimoDia.getDate(); dia++) {
        const data = new Date(ano, mes, dia)

        // Formato YYYY-MM-DD (compatível com backend)
        const dataFormatada = data.toISOString().split("T")[0]

        const div = document.createElement("div")
        div.classList.add("dia")
        div.innerText = dia

        // Marca dias que possuem viagens
        if (datasViagens.includes(dataFormatada)) {
            div.classList.add("tem-viagem")

            // Clique leva para listagem filtrada por data
            div.addEventListener("click", () => {
                window.location.href = `/viagens?data=${dataFormatada}`
            })
        }

        calendario.appendChild(div)
    }
}

// Atualiza o título do calendário (mês/ano)
function atualizarTitulo(ano, mes) {
    const meses = [
        "Janeiro", "Fevereiro", "Março", "Abril",
        "Maio", "Junho", "Julho", "Agosto",
        "Setembro", "Outubro", "Novembro", "Dezembro"
    ]

    document.getElementById("mes-ano").innerText =
        `${meses[mes]} de ${ano}`
}

// Avança para o próximo mês
function proximoMes() {
    dataAtual.setMonth(dataAtual.getMonth() + 1)
    gerarCalendario()
}

// Volta para o mês anterior
function mesAnterior() {
    dataAtual.setMonth(dataAtual.getMonth() - 1)
    gerarCalendario()
}

// Inicializa o calendário ao carregar a página
gerarCalendario()