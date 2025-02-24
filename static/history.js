// Sahifa refreshdan so'ng modalni yopiq qilish
$("#orderDetailModal").hide();

$(document).ready(function () {
    // Modalni ochish
    $(".detail-btn").click(function () {
        const orderId = $(this).data("order-id");

        // Serverga AJAX so'rov
        $.ajax({
            url: `/order/details/${orderId}/`, // URLni moslashtiring
            method: "GET",
            success: function (data) {
                // Modal ichiga ma'lumotlarni yuklash
                let modalContent = "";
                data.items.forEach(item => {
                    modalContent += `
                    <tr>
                        <td><img src="${item.image_url}" alt="${item.product_name}" width="50"></td>
                        <td>${item.product_name}</td>
                        <td>${item.size}</td>
                        <td>${item.quantity}</td>
                        <td>${item.price}</td>
                    </tr>
                `;
                });
                $("#modal-body").html(modalContent);
                $("#orderDetailModal").fadeIn();
            },
            error: function () {
                alert("Ma'lumotlarni yuklashda xatolik yuz berdi.");
            }
        });
    });


    // Modalni yopish
    $(".close").click(function () {
        $("#orderDetailModal").fadeOut();
    });

    $(window).click(function (event) {
        if ($(event.target).is("#orderDetailModal")) {
            $("#orderDetailModal").fadeOut();
        }
    });
});

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
