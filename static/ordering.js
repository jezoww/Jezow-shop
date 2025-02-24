function showAddressOptions() {
    document.getElementById('address-options').style.display = 'block';
}

function updateAddress() {
    const selectedAddress = document.getElementById('address-dropdown').value;
    document.getElementById('current-address').innerHTML = selectedAddress;
    document.getElementById('address-options').style.display = 'none';
}

function showMap() {
    document.getElementById('map-container').style.display = 'block';

    const map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: -34.397, lng: 150.644},
        zoom: 8,
    });

    const autocomplete = new google.maps.places.Autocomplete(document.getElementById('new-address'));

    autocomplete.addListener('place_changed', function () {
        const place = autocomplete.getPlace();
        document.getElementById('new-address').value = place.formatted_address;
    });
}

function confirmNewAddress() {
    const newAddress = document.getElementById('new-address').value;
    const dropdown = document.getElementById('address-dropdown');

    if (newAddress) {
        const option = document.createElement('option');
        option.text = newAddress;
        option.value = newAddress;
        dropdown.add(option);
        dropdown.value = newAddress;
        updateAddress();
        document.getElementById('map-container').style.display = 'none';
    }
}

function showAddressOptions() {
    document.getElementById('address-options').style.display = 'block';
}

function addNewAddress() {
    const newAddressInput = document.getElementById('new-address');
    const newAddress = newAddressInput.value.trim();

    if (newAddress) {
        // Manzilni tanlash qutisiga qo'shish
        const addressDropdown = document.getElementById('address-dropdown');
        const newOption = document.createElement('option');
        newOption.value = newAddress;
        newOption.textContent = newAddress;
        addressDropdown.appendChild(newOption);

        // Manzilni darhol tanlash
        addressDropdown.value = newAddress;
        updateAddress();

        // Input maydonini tozalash va uni yashirish
        newAddressInput.value = '';
        document.getElementById('new-address-input').style.display = 'none';
    } else {
        alert('Iltimos, manzilni kiriting.');
    }
}

function updateAddress() {
    const selectedAddress = document.getElementById('address-dropdown').value;
    const currentAddress = document.getElementById('selected-address');
    currentAddress.textContent = selectedAddress;

    // Tanlangan manzilni birinchi variant sifatida belgilash
    document.getElementById('address-dropdown').value = selectedAddress;

    // Dropdownni yashirish
    document.getElementById('address-options').style.display = 'none';
}

// Xabarlarni 3 soniyadan keyin yashirish
document.addEventListener('DOMContentLoaded', function () {
    setTimeout(function () {
        const messages = document.querySelectorAll('.fade-message');
        messages.forEach(function (message) {
            message.style.transition = 'opacity 0.5s ease';
            message.style.opacity = '0';
            setTimeout(() => message.remove(), 500); // Animatsiya tugagach, elementni o'chirish
        });
    }, 3000); // 3 soniya
});
