// Pega o input de telefone pelo ID
const telefoneInput = document.getElementById('telefone');

// Remove tudo que não for número
function apenasNumeros(valor){
    return valor.replace(/\D/g, "");
}

// Aplica a máscara de telefone
function formatarTelefone(valor){

    let numero = apenasNumeros(valor);

    // Telefone fixo (até 10 dígitos)
    if(numero.length <= 10){

        // (00) 0000-0000
        numero = numero.replace(/^(\d{2})(\d)/g, "($1) $2");
        numero = numero.replace(/(\d{4})(\d)/, "$1-$2");

    }else{

        // Celular (11 dígitos)
        // (00) 00000-0000
        numero = numero.replace(/^(\d{2})(\d)/g, "($1) $2");
        numero = numero.replace(/(\d{5})(\d)/, "$1-$2");

    }

    return numero;
}

// Evento disparado enquanto o usuário digita
telefoneInput.addEventListener("input", function(){
    this.value = formatarTelefone(this.value);
});