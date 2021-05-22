let submitButton = document.querySelector("#submit-button")
let passwordInput = document.querySelector("#user_password")
let passwordRepeat = document.querySelector("#user_password_repeat")
let form = document.querySelector("form")
let user_name = document.querySelector("#user_name")
let user_surname = document.querySelector("#user_surname")
let user_email = document.querySelector("#user_email")
let user_phone = document.querySelector("#user_phone")
let loginError = document.querySelector(".login-error")

submitButton.disabled = true


passwordRepeat.oninput = function () {
    if (passwordRepeat.value === passwordInput.value && passwordInput.value !== "") {
        submitButton.disabled = false;
        passwordInput.style.backgroundColor = "white";
        passwordRepeat.style.backgroundColor = "white";
    } else {
        submitButton.disabled = true;
        passwordInput.style.backgroundColor = "rgb(255,168,168)";
        passwordRepeat.style.backgroundColor = "rgb(255,168,168)";
    }
}

form.onsubmit = async function(e) {
    e.preventDefault();
    let request = {
        "jsonrpc": "2.0",
        "method": "register",
        "params": {
            "user_name": user_name.value,
            "user_surname": user_surname.value,
            "user_email": user_email.value,
            "user_phone": user_phone.value,
            "user_password": passwordInput.value
        },
        "id": "test"
    }

    let response = await fetch(window.location.origin + '/api/v1/jsonrpc', {
            method: "POST",
            body: JSON.stringify(request)
        });
        let result = await response.json()
        if(result.result != null){
            window.location.replace(window.location.origin + '/auth/login')
        }
        else if(result.error){
            loginError.textContent = result.error.message
        }
}
