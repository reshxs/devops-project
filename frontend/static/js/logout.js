logoutButton = document.querySelector(".logout-button");
let base_url = window.location.origin;

logoutButton.onclick = async function(){
    console.log("logout")
    let request = {
        "jsonrpc": "2.0",
        "method": "logout",
        "id": "test"
    };

    let response = await fetch(base_url + "/api/v1/jsonrpc", {
        "method": "POST",
        "body": JSON.stringify(request)
    });

    let result = await response.json()
    if(result.result != null){
        window.location.reload();
    }
}