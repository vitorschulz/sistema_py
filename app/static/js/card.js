    window.addEventListener("pageshow", function(event) {
    if (event.persisted) {
        window.location.reload();
    }
});


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

document.addEventListener("click", function(){

    document.querySelectorAll(".menu-opcoes").forEach(o=>{
        o.style.display = "none"
    })

    document.querySelectorAll(".card-viagem").forEach(c=>{
        c.classList.remove("menu-aberto")
    })

})