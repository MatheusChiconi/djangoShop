document.addEventListener("DOMContentLoaded", function () {
    const editBtn = document.getElementById("editBtn");
    const saveBtn = document.getElementById("saveBtn");
    const inputs = document.querySelectorAll("form input");

    editBtn.addEventListener("click", function () {
        inputs.forEach(input => {
            // Mantém email e cpf como somente leitura se quiser
            if (!["email", "cpf"].includes(input.id)) {
                input.removeAttribute("readonly");
            }
        });
        saveBtn.disabled = false;
    });
});

// Substitui "None" por "Adicione" nos campos de entrada
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll('.account-card input').forEach(function(input) {
        if (input.value === "None") {
            input.value = "Vazio";
        }
    });
});