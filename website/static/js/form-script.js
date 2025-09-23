let eyeSpriteUrl = null;

document.addEventListener("DOMContentLoaded", () => {
    const validation_forms = document.querySelectorAll('form.needs-validation');

    for (const form of validation_forms) {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            } else {
                handleFormSubmission(form);
            }

            form.classList.add('was-validated');
        }, false)
    }

    const metaEyeSpriteUrl = document.querySelector('meta[name=eye-sprite-url]')
    if (metaEyeSpriteUrl === null) {
        return;
    }
    eyeSpriteUrl = metaEyeSpriteUrl.content;

    const visibilityToggles = document.querySelectorAll('button.password-visibility-toggle');
    Array.from(visibilityToggles).forEach(button => {
        button.addEventListener("click", togglePasswordVisibility);
    })

    const passwordInput = document.getElementById("password");
    if (passwordInput === null || passwordInput.tagName !== "INPUT") {
        return;
    }
    const confirmPasswordInput = document.getElementById("confirm_password");
    if (confirmPasswordInput === null || confirmPasswordInput.tagName !== "INPUT") {
        return;
    }

    const validatePasswordMatch = () => {
        if (confirmPasswordInput.value !== passwordInput.value) {
            confirmPasswordInput.setCustomValidity("Passwords do not match");
        } else {
            confirmPasswordInput.setCustomValidity("");
        }
    };

    passwordInput.addEventListener('input', validatePasswordMatch);
    confirmPasswordInput.addEventListener('input', validatePasswordMatch);
});

function togglePasswordVisibility() {
    const inputField = this.parentElement.querySelector("input");
    if (inputField === null) {
        throw new Error("The visibility toggle is not utilizing the expected layout.");
    }

    if (inputField.getAttribute("type") === "password") {
        inputField.setAttribute("type", "text");
        this.querySelector("use").setAttribute("href", `${eyeSpriteUrl}#icon-eye-slash`);
        return;
    }

    inputField.setAttribute("type", "password");
    this.querySelector("use").setAttribute("href", `${eyeSpriteUrl}#icon-eye`);
}

/**
 * 
 * @param {HTMLFormElement} form 
 */
function handleFormSubmission(form) {
    const submitButton = form.querySelector('[type="submit"]');
    submitButton.disabled = true;
}