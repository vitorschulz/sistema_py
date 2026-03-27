document.addEventListener("submit", function(e) {
    const form = e.target;

    if (form.method.toLowerCase() === "get") return;

    if (form.hasAttribute("data-validate-tipo")) return;
    if (form.hasAttribute("data-no-disable")) return;

    const btn = form.querySelector("button[type='submit']");
    if (btn) {
        btn.disabled = true;
        btn.dataset.originalText = btn.innerText;
        btn.innerText = "Salvando...";
    }
});

document.addEventListener('click', function(e) {
    const btn = e.target.closest('.btn-excluir, .btn-compensar, .btn-devolver');
    if (!btn) return;

    e.preventDefault();
    e.stopPropagation(); 
    if (btn.classList.contains("js-excluir-financeiro")) return;
    if (btn.dataset.clicked) return;

   if (btn.dataset.confirm) {
        const confirmar = confirm(btn.dataset.confirm);
        if (!confirmar) return;
    }


    btn.dataset.clicked = "true";
    btn.style.pointerEvents = "none";
    btn.style.opacity = "0.6";

    if (btn.href) {
    window.location.assign(btn.href);
}
});

document.addEventListener('click', function(e) {
    const btn = e.target.closest('.btn-excluir-rapido');
    if (!btn) return;

    if (btn.dataset.clicked) {
        e.preventDefault();
        return;
    }

    btn.dataset.clicked = "true";
    btn.style.pointerEvents = "none";
    btn.style.opacity = "0.6";
});