const telefoneInput = document.getElementById('telefone');

function apenasNumeros(valor){
    return valor.replace(/\D/g, "");
}

function formatarTelefone(valor){

    let numero = apenasNumeros(valor);

    if(numero.length <= 10){

        numero = numero.replace(/^(\d{2})(\d)/g, "($1) $2");
        numero = numero.replace(/(\d{4})(\d)/, "$1-$2");

    }else{

        numero = numero.replace(/^(\d{2})(\d)/g, "($1) $2");
        numero = numero.replace(/(\d{5})(\d)/, "$1-$2");

    }

    return numero;
}

telefoneInput.addEventListener("input", function(){
    this.value = formatarTelefone(this.value);
});