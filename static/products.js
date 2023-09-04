document.addEventListener("DOMContentLoaded", function() {

    // Запрос товаров
    function fetchProducts(filters = {}) {
        let url = "http://45.12.72.104/products/";

        if (Object.keys(filters).length > 0) {
            const queryParams = new URLSearchParams(filters);
            url += "?" + queryParams.toString();
        }

        fetch(url)
            .then(response => response.json())
            .then(data => populateProductList(data))
            .catch(error => console.error("Error fetching products:", error));
    }

    // Наполнение html товарами
    function populateProductList(products) {
        const productList = document.getElementById("product-list");
        productList.innerHTML = ""; // Очищаем текущий список

        if (products.length === 0) {
            const noProductsDiv = document.createElement("div");
            noProductsDiv.className = "no-products";
            noProductsDiv.textContent = "Нет доступных товаров";
            productList.appendChild(noProductsDiv);
            return;
        }

        console.log(products)
        products.forEach(product => {
            const productCard = document.createElement("div");
            productCard.className = "product-card";

            const nameDiv = document.createElement("div");
            nameDiv.className = "product-param";
            nameDiv.textContent = `Наименование: ${product.name}`;

            const typeDiv = document.createElement("div");
            typeDiv.className = "product-param";
            typeDiv.textContent = `Тип: ${product.type}`;

            const priceDiv = document.createElement("div");
            priceDiv.className = "product-param";
            priceDiv.textContent = `Стоимость: ${product.price}`;

            const dateDiv = document.createElement("div");
            dateDiv.className = "product-param";
            dateDiv.textContent = `Дата: ${product.date}`;

            const weightDiv = document.createElement("div");
            weightDiv.className = "product-param";
            weightDiv.textContent = `Вес: ${product.weight}`;

            const sizeDiv = document.createElement("div");
            sizeDiv.className = "product-param";
            sizeDiv.textContent = `Размер: ${product.height}x${product.width}x${product.depth}`;

            const manufacturerDiv = document.createElement("div");
            manufacturerDiv.className = "product-param";
            manufacturerDiv.textContent = `Производитель: ${product.manufacturer}`;

            productCard.appendChild(nameDiv);
            productCard.appendChild(typeDiv);
            productCard.appendChild(priceDiv);
            productCard.appendChild(dateDiv);
            productCard.appendChild(weightDiv);
            productCard.appendChild(sizeDiv);
            productCard.appendChild(manufacturerDiv);

            productList.appendChild(productCard);
        });
    }


    // Привязка к кнопке функции запроса товаров
    const applyFiltersButton = document.getElementById("applyFilters");

    applyFiltersButton.addEventListener("click", function() {
        const filters = {
            name: document.getElementById("nameFilter").value,
            type: document.getElementById("typeFilter").value,
            manufacturer: document.getElementById("manufacturerFilter").value,
            min_price: document.getElementById("minPriceFilter").value,
            max_price: document.getElementById("maxPriceFilter").value,
        };

        Object.keys(filters).forEach(key => {
            if (filters[key] === "None") {
                delete filters[key];
            }
        });
        fetchProducts(filters);
    });

    // Экспорт в пдф
    const exportToPdfButton = document.getElementById("exportToPdf");

    exportToPdfButton.addEventListener("click", function() {
        const products = document.querySelectorAll(".product-card");
        const content = [];

        products.forEach((product, index) => {
            const productInfo = [];
            const params = product.querySelectorAll(".product-param");
            params.forEach(param => {
                productInfo.push(param.textContent);
            });
            content.push({ text: `Товар ${index + 1}:\n`, bold: true });
            content.push(productInfo.join("\n"));
            content.push({ text: '\n', margin: [0, 0, 0, 10] });
        });

        const docDefinition = {
            content: content,
            defaultStyle: {
                font: "Roboto"
            }
        };

        pdfMake.createPdf(docDefinition).download("products.pdf");
    });


    // Запрос товаров при загрузке страницы
    fetchProducts();

    // Наполнение фильтров
    function fetchUniqueValues(endpoint, elementId) {
        fetch(`http://45.12.72.104/${endpoint}/`)
            .then(response => response.json())
            .then(data => {
                const selectElement = document.getElementById(elementId);
                data[endpoint].forEach(value => {
                    const option = document.createElement("option");
                    option.value = value;
                    option.textContent = value;
                    selectElement.appendChild(option);
                });
            })
            .catch(error => console.error(`Error fetching ${endpoint}:`, error));
    }

    // Запрос значение для типов и производителей
    fetchUniqueValues('types', 'typeFilter');
    fetchUniqueValues('manufacturers', 'manufacturerFilter');
});
