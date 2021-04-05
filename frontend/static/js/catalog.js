let catalogList = document.querySelector(".catalog-list")


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
                let listElement = document.createElement('li');
                listElement.classList.add('product-card');
                listElement.classList.add('search-item');

                let title = document.createElement('a');
                title.href='#';
                title.classList.add('product-title');
                title.textContent = product.product_name;
                listElement.append(title);

                let img = document.createElement('img');
                img.src = product.product_img_url;
                img.classList.add('catalog-product-img')
                listElement.append(img)

                let price = document.createElement('p');
                price.classList.add('product-price');
                price.textContent = '$' + product.product_price;
                listElement.append(price);

                let cart_button = document.createElement('p');
                cart_button.classList.add('catalog-add-to-card-button');
                cart_button.textContent = 'В корзину';
                listElement.append(cart_button);
                cart_button.onclick = async function() {
                    let request = {
                        "jsonrpc": "2.0",
                        "method": "add_to_cart",
                        "params": {
                            "product_id": product.product_id,
                            "count": 1
                        },
                        "id": "test"
                    };

                    let response = await fetch("http://localhost/api/v1/jsonrpc", {
                        "method": "POST",
                        "body": JSON.stringify(request)
                    });

                    let result = await response.json();
                    if(result.result != null){
                        window.location = "http://localhost/cart";
                    } else {
                        console.log(result.error.message)
                    }
                }

                catalogList.append(listElement);
            }
        }
}