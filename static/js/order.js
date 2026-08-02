const quantityInputs = document.querySelectorAll(".quantity");

const totalItems = document.getElementById("total-items");

const grandTotal = document.getElementById("grand-total");

function updateSummary(){

    let items = 0;

    let total = 0;

    quantityInputs.forEach(input =>{

        const quantity = parseFloat(input.value) || 0;

        const price = parseFloat(input.dataset.price);

        items += quantity;

        total += quantity * price;

    });

    totalItems.textContent = items;

    grandTotal.textContent = total.toLocaleString();

}

quantityInputs.forEach(input =>{

    input.addEventListener("input", updateSummary);

});

updateSummary();
