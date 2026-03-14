const shopping = document.getElementById("shopping")
const loja = document.getElementById("loja")

function filtrarLojas(){

    const shoppingId = shopping.value

    for(let option of loja.options){

        const lojaShopping = option.dataset.shopping

        option.style.display =
            lojaShopping == shoppingId ? "block" : "none"

    }

}

shopping.addEventListener("change", filtrarLojas)

filtrarLojas()