    let button = document.querySelector('#login-button')
    let emailInput = document.querySelector('#email-input')
    let passwordInput = document.querySelector('#password-input')
    let next_url_input = document.querySelector('#next_url')
    let loginError = document.querySelector('.login-error')
    let next_url = next_url_input.value

    button.onclick = async function () {
        let email = emailInput.value;
        let password = passwordInput.value;
        let request = {
            "jsonrpc": "2.0",
            "method": "login",
            "params": [{
                "email": email,
                "password": password
            }],
            "id": "login"
        };

        let response = await fetch('http://127.0.0.1:8080/api/v1/jsonrpc', {
            method: "POST",
            body: JSON.stringify(request)
        });
        let result = await response.json()
        if(result.result != null){
            window.location.replace(next_url)
        }
        else if(result.error){
            loginError.textContent = result.error.message
        }
    };