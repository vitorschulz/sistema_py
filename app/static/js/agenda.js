
const datasViagens = JSON.parse(
    document.getElementById("datas-viagens").textContent
)


let dataAtual = new Date()

function gerarCalendario() {
    const ano = dataAtual.getFullYear()
    const mes = dataAtual.getMonth()

    const ultimoDia = new Date(ano, mes + 1, 0)

    const calendario = document.getElementById("calendario")
    calendario.innerHTML = ""

    atualizarTitulo(ano, mes)

    for (let dia = 1; dia <= ultimoDia.getDate(); dia++) {
        const data = new Date(ano, mes, dia)

        const dataFormatada = data.toLocaleDateString("en-CA")

        const div = document.createElement("div")
        div.classList.add("dia")
        div.innerText = dia

        if (datasViagens.includes(dataFormatada)) {
            div.classList.add("tem-viagem")

            div.addEventListener("click", () => {
                window.location.href = `/viagens?data=${dataFormatada}`
            })
        }

        calendario.appendChild(div)
    }
}


function atualizarTitulo(ano, mes) {
    const meses = [
        "Janeiro", "Fevereiro", "Março", "Abril",
        "Maio", "Junho", "Julho", "Agosto",
        "Setembro", "Outubro", "Novembro", "Dezembro"
    ]

    document.getElementById("mes-ano").innerText =
        `${meses[mes]} de ${ano}`
}


function proximoMes() {
    dataAtual.setMonth(dataAtual.getMonth() + 1)
    gerarCalendario()
}


function mesAnterior() {
    dataAtual.setMonth(dataAtual.getMonth() - 1)
    gerarCalendario()
}


gerarCalendario()