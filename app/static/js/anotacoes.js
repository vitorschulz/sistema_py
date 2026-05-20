(function () {
    const toggle = document.getElementById('toggle-anotacao');
    const campos = document.getElementById('campos-tarefa');
    const form = document.querySelector('form');
    const obsTextarea = form.querySelector('textarea[name="observacoes"]');

    // hidden que vai pro POST
    let hiddenAnotacao = form.querySelector('input[name="anotacao"]');
    if (!hiddenAnotacao) {
        hiddenAnotacao = document.createElement('input');
        hiddenAnotacao.type = 'hidden';
        hiddenAnotacao.name = 'anotacao';
        form.appendChild(hiddenAnotacao);
    }

    function aplicar() {
        const ativo = toggle.checked;

        const clienteSelect = campos.querySelector('select[name="cliente_id"]');
        const tipoCheckboxes = campos.querySelectorAll('input[name="tipo[]"]');

        if (clienteSelect) clienteSelect.disabled = ativo;
        tipoCheckboxes.forEach(cb => cb.disabled = ativo);
        if (obsTextarea) obsTextarea.disabled = ativo;

        const grupoCliente = clienteSelect?.closest('.form-group');
        const grupoTipo = campos.querySelector('.checkbox-group')?.closest('.form-group');
        const grupoObs = obsTextarea?.closest('.form-group');

        if (grupoCliente) grupoCliente.style.opacity = ativo ? '0.4' : '1';
        if (grupoTipo) grupoTipo.style.opacity = ativo ? '0.4' : '1';
        if (grupoObs) grupoObs.style.opacity = ativo ? '0.4' : '1';

        hiddenAnotacao.value = ativo ? '1' : '0';

        if (ativo) {
            form.setAttribute('data-anotacao', '1');
        } else {
            form.removeAttribute('data-anotacao');
        }
    }

    toggle.addEventListener('change', aplicar);
    aplicar();
})();