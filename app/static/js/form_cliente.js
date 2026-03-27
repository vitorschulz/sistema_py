// Seleciona os inputs
const cpfCnpjInput = document.getElementById("cpf_cnpj");
const telefoneInput = document.querySelector("input[name='telefone']");

// Remove tudo que não for número
function apenasNumeros(valor){
    return valor.replace(/\D/g, "");
}

// Formata CPF ou CNPJ automaticamente
function formatarCpfCnpj(valor){

    let numero = apenasNumeros(valor);

    // CPF (até 11 dígitos)
    if(numero.length <= 11){

        numero = numero.replace(/(\d{3})(\d)/, "$1.$2");
        numero = numero.replace(/(\d{3})(\d)/, "$1.$2");
        numero = numero.replace(/(\d{3})(\d{1,2})$/, "$1-$2");
    
    // CNPJ (14 dígitos)
    }else{

        numero = numero.replace(/^(\d{2})(\d)/, "$1.$2");
        numero = numero.replace(/^(\d{2})\.(\d{3})(\d)/, "$1.$2.$3");
        numero = numero.replace(/\.(\d{3})(\d)/, ".$1/$2");
        numero = numero.replace(/(\d{4})(\d)/, "$1-$2");

    }

    return numero;
}

// Formata telefone (fixo ou celular)
function formatarTelefone(valor){

    let numero = apenasNumeros(valor);

    // (00) 0000-0000
    if(numero.length <= 10){

        numero = numero.replace(/^(\d{2})(\d)/g, "($1) $2");
        numero = numero.replace(/(\d{4})(\d)/, "$1-$2");
    
    // (00) 00000-0000
    }else{

        numero = numero.replace(/^(\d{2})(\d)/g, "($1) $2");
        numero = numero.replace(/(\d{5})(\d)/, "$1-$2");

    }

    return numero;
}

// Aplica máscara enquanto digita (CPF/CNPJ)
cpfCnpjInput.addEventListener("input", function(){
    this.value = formatarCpfCnpj(this.value);
});

// Aplica máscara enquanto digita (telefone)
telefoneInput.addEventListener("input", function(){
    this.value = formatarTelefone(this.value);
});