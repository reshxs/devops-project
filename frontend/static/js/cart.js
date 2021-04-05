let cartItemsList = document.querySelector(".cart-items-list")
let cartProductsCount = document.querySelector(".cart-products-count")


window.onload = async function(){
    let request = {
        "jsonrpc": "2.0",
        "method": "get_cart",
        "id": "test"
    };

    let response = await fetch('http://localhost:80/api/v1/jsonrpc', {
            method: "POST",
            body: JSON.stringify(request)
    });
    let result = await response.json();
    if(result.result !== undefined) {
        let items = Object.getOwnPropertyNames(result.result);
        for (let productId of items){
            let product = result.result[productId].product
            let newElement = document.createElement('li');
            newElement.classList.add('cart-item')

            let title = document.createElement('h2');
            title.classList.add('cart-item-element');
            title.textContent = product.product_name;
            newElement.append(title)

            let price = document.createElement('p');
            price.classList.add('cart-item-element');
            price.textContent = 'Стоимость: ' + product.product_price;
            newElement.append(price);

            let count_label = document.createElement('p');
            count_label.classList.add('cart-item-element');
            count_label.textContent = 'Количество: ';
            newElement.append(count_label);

            let count_input = document.createElement('input');
            count_input.type = 'number';
            count_input.classList.add('cart-item-element');
            count_input.classList.add('cart-count-input');
            count_input.value = result.result[productId].count;
            newElement.append(count_input);

            let actual_price = document.createElement('p');
            actual_price.classList.add('cart-item-element');
            actual_price.textContent = 'Цена: ' + product.product_price * result.result[productId].count;
            newElement.append(actual_price);

            let delete_button = document.createElement('p');
            delete_button.classList.add('cart-delete-btn');
            delete_button.textContent = 'X';
            newElement.append(delete_button);

            cartItemsList.append(newElement);

            count_input.onchange = async function(){
                console.log('change')
                let request = {
                    "jsonrpc": "2.0",
                    "method": "change_product_count",
                    "params": {
                        "product_id": productId,
                        "count": count_input.value
                    },
                    "id": "test"
                };

                let response = await fetch("http://localhost/api/v1/jsonrpc", {
                    method: "POST",
                    body: JSON.stringify(request)
                });

                let result = await response.json();
                if (result.result != null) {
                    actual_price.textContent = 'Цена: ' + count_input.value * product.product_price;
                }
            }

            delete_button.onclick = async function(){
                let request = {
                    "jsonrpc": "2.0",
                    "method": "remove_from_cart",
                    "params": {
                        "product_id": productId
                    },
                    "id": "test"
                };

                let response = await fetch("http://localhost/api/v1/jsonrpc", {
                    method: "POST",
                    body: JSON.stringify(request)
                });

                let result = await response.json();
                if (result.result != null){
                    cartItemsList.removeChild(newElement);
                    items.pop(productId);
                    cartProductsCount.textContent = items.length;
                }
            }
        }

        cartProductsCount.textContent = items.length;
        console.log(items.length);
    } else {
        cartProductsCount.textContent = '0';
        console.log(result.error.message);
    }
}