let productsList = document.querySelector(".product-list")


window.onload = async function (){
    let request = {
            "jsonrpc": "2.0",
            "method": "products_list",
            "id": "login"
        };

        let response = await fetch('http://localhost:80/api/v1/jsonrpc', {
            method: "POST",
            body: JSON.stringify(request)
        });
        let result = await response.json();

        if(result.result != null){
            for (let product of result.result){
                let newProduct = document.createElement('li');
                newProduct.textContent = product.product_name
                productsList.append(newProduct)
            }
        }
}