const cpfCnpjInput = document.getElementById("cpf_cnpj");
const telefoneInput = document.querySelector("input[name='telefone']");

function apenasNumeros(valor){
    return valor.replace(/\D/g, "");
}

function formatarCpfCnpj(valor){

    let numero = apenasNumeros(valor);

    if(numero.length <= 11){

        numero = numero.replace(/(\d{3})(\d)/, "$1.$2");
        numero = numero.replace(/(\d{3})(\d)/, "$1.$2");
        numero = numero.replace(/(\d{3})(\d{1,2})$/, "$1-$2");

    }else{

        numero = numero.replace(/^(\d{2})(\d)/, "$1.$2");
        numero = numero.replace(/^(\d{2})\.(\d{3})(\d)/, "$1.$2.$3");
        numero = numero.replace(/\.(\d{3})(\d)/, ".$1/$2");
        numero = numero.replace(/(\d{4})(\d)/, "$1-$2");

    }

    return numero;
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

cpfCnpjInput.addEventListener("input", function(){
    this.value = formatarCpfCnpj(this.value);
});

telefoneInput.addEventListener("input", function(){
    this.value = formatarTelefone(this.value);
});