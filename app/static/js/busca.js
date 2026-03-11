function filtrarTabela() {

    let input = document.getElementById("campo-busca");
    let filtro = input.value.toLowerCase();

    let tabela = document.getElementById("tabela-lista");
    let linhas = tabela.getElementsByTagName("tr");

    for (let i = 1; i < linhas.length; i++) {

        let colunas = linhas[i].getElementsByTagName("td");
        let encontrou = false;

        for (let j = 0; j < colunas.length; j++) {

            let texto = colunas[j].textContent || colunas[j].innerText;

            if (texto.toLowerCase().includes(filtro)) {
                encontrou = true;
                break;
            }

        }

        if (encontrou) {
            linhas[i].style.display = "";
        } else {
            linhas[i].style.display = "none";
        }

    }

}