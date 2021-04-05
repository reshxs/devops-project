let input = document.querySelector('.search-input')
let items = document.querySelectorAll('.search-item')


input.oninput = function (){
    if (items.length === 0){
        items = document.querySelectorAll('.search-item')
    }
    let value = input.value.toLowerCase();
    for (let item of items){
        item.classList.add('hidden')
        for(let node of item.childNodes){
            if (node.textContent.toLowerCase().indexOf(value) !== -1){
                item.classList.remove('hidden')
            }
        }
        if (item.textContent.toLowerCase().indexOf(value) === -1){
            item.classList.add('hidden')
        }
    }
}