let items = document.querySelectorAll('.search-item')
let input = document.querySelector('.search-input')


input.oninput = function (){
    let value = input.value.toLowerCase();
    for (let item of items){
        if (item.textContent.toLowerCase().indexOf(value) === -1){
            item.classList.add('hidden')
        } else {
            item.classList.remove('hidden')
        }
    }
}