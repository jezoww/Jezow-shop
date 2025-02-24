function decreaseQuantity(button) {
    var quantityInput = button.nextElementSibling;
    if (quantityInput.value > 1) {
        quantityInput.value--;
        updateSubtotal(quantityInput.id.split('-').pop());
    }
}

function increaseQuantity(button) {
    var quantityInput = button.previousElementSibling;
    quantityInput.value++;
    updateSubtotal(quantityInput.id.split('-').pop());
}

function updateSubtotal(productId) {
    var quantityInput = document.getElementById('quantity-input-' + productId);
    var quantity = quantityInput.value;
    var price = parseFloat(document.querySelector('#quantity-input-' + productId).closest('tr').querySelector('.product-price').textContent);
    var subtotal = price * quantity;

    // Update the subtotal field
    document.querySelector('#quantity-input-' + productId).closest('tr').querySelector('.product-subtotal').textContent = subtotal + " so'm";
}

function updateCartTotals() {
    let total = 0;

    const cartRows = document.querySelectorAll('.cart-table tbody tr');
    cartRows.forEach(row => {
        const priceElement = row.querySelector('.product-price');
        const quantityInput = row.querySelector('.quantity-input');
        const subtotalElement = row.querySelector('.product-subtotal');

        const price = parseFloat(priceElement.innerText.replace('$', ''));
        const quantity = parseInt(quantityInput.value);
        const subtotal = price * quantity;

        subtotalElement.innerText = `$${subtotal.toFixed(2)}`;
        total += subtotal;
    });

    document.getElementById('subtotal').innerText = `$${total.toFixed(2)}`;
    document.getElementById('total').innerText = `$${total.toFixed(2)}`;
}

// Sahifa yangilanishini to'xtatish va modalni ochish
document.getElementById("phoneIcon").addEventListener("click", function (event) {
    event.preventDefault(); // Sahifa yangilanishini to'xtatadi
    openModal(); // Modalni ochadi
});

function openModal() {
    var modal = document.getElementById("phoneModal");
    modal.style.display = "block";
}

function closeModal() {
    var modal = document.getElementById("phoneModal");
    modal.style.display = "none";
}

// Nusxalash funksiyasi
document.getElementById("copyButton").addEventListener("click", function (event) {
    event.preventDefault(); // Tugma bosilganda sahifa yangilanmasligi uchun

    var phoneNumber = document.getElementById("phoneNumber").textContent;
    var tempInput = document.createElement("input");
    tempInput.value = phoneNumber;
    document.body.appendChild(tempInput);
    tempInput.select();
    document.execCommand("copy");
    document.body.removeChild(tempInput);

    // Nusxalandi xabarini chiqarish
    var copyMessage = document.getElementById("copyMessage");
    copyMessage.style.display = "block";

    // 2 soniyadan keyin nusxalandi yozuvi yashirinadi va modal oynasi yopiladi
    setTimeout(function () {
        copyMessage.style.display = "none";
        closeModal(); // Modal oynasini yopadi
    }, 2000); // 2 soniya kutadi
});

document.addEventListener('DOMContentLoaded', function () {
    updateCartTotals();

    const quantityInputs = document.querySelectorAll('.quantity-input');
    quantityInputs.forEach(input => {
        input.addEventListener('change', function () {
            updateCartTotals();
        });
    });

    const quantityButtons = document.querySelectorAll('.quantity-button');
    quantityButtons.forEach(button => {
        button.addEventListener('click', function () {
            updateCartTotals();
        });
    });
});

function toggleDropdown() {
    var dropdown = document.getElementById("userDropdown");
    dropdown.classList.toggle("show");
}

// Dropdownni yopish uchun sahifadagi boshqa joyni bosganingizda ishlatiladi
window.onclick = function (event) {
    if (!event.target.matches('.user-icon, .user-icon *')) {
        var dropdowns = document.getElementsByClassName("dropdown-content");
        for (var i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            }
        }
    }
}

function showAddressOptions() {
    document.getElementById('address-options').style.display = 'block';
}




document.addEventListener('DOMContentLoaded', function () {
    console.log("JavaScript ishlamoqda!");

    // 3 soniyadan so'ng barcha alertlarni yo'q qilish
    setTimeout(function () {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(function (alert) {
            alert.classList.remove('show'); // Bootstrap `show` klassini olib tashlaymiz
            alert.classList.add('fade');   // Bootstrap `fade` klassini qo'shamiz
            setTimeout(() => alert.remove(), 500); // Animatsiya tugagach, elementni o'chirish
        });
    }, 2000); // 3 soniya
});



let currentIndex = 0;

function showSlide(index) {
    const slides = document.querySelectorAll('.slide');
    const totalSlides = slides.length;

    if (index >= totalSlides) {
        currentIndex = 0;
    } else if (index < 0) {
        currentIndex = totalSlides - 1;
    } else {
        currentIndex = index;
    }

    const offset = -currentIndex * 100;
    document.querySelector('.slides').style.transform = `translateX(${offset}%)`;
}

function nextSlide() {
    showSlide(currentIndex + 1);
}

function prevSlide() {
    showSlide(currentIndex - 1);
}

// Automatik ravishda o'zgarish
setInterval(() => {
    nextSlide();
}, 3000);

// Sahifa yuklanganda birinchi slaydni ko'rsating
showSlide(currentIndex);