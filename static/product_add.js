document.addEventListener("DOMContentLoaded", function() {
    // Находим форму, где пользователь вводит данные товара
    const form = document.getElementById("product-form");

    // Добавляем прослушиватель события
    form.addEventListener("submit", function(event) {
        // Прерываем дефолтное выполнение отправки формы
        event.preventDefault();

        // Создаем объект товара
        const product = {
            name: form.name.value,
            type: form.type.value,
            price: parseFloat(form.price.value),
            date: form.date.value,
            weight: parseFloat(form.weight.value),
            height: parseFloat(form.height.value),
            width: parseFloat(form.width.value),
            depth: parseFloat(form.depth.value),
            manufacturer: form.manufacturer.value,
        };

        // Отправляем POST запрос
        fetch("http://127.0.0.1:8000/product/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(product),
        })
        .then(response => response.json())
        .then(data => {
            if (data.message === "Product created successfully") {
                alert("Товар успешно добавлен!");
            } else {
                alert("Произошла ошибка при добавлении товара!");
            }
        })
        .catch(error => {
            console.error("There was a problem with the fetch operation:", error);
        });
    });
});
