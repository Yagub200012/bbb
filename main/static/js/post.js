document.getElementById('PostForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Остановить стандартную отправку формы

    let title = document.getElementById('title').value;
    let content = document.getElementById('content').value;
    let subsector = document.getElementById('subsector').value;
    const accessToken = getCookie('access_token');


    // Отправляем запрос на API
    fetch('/api/post_create/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}',
            'Authorization': `Bearer ${accessToken}`
        },
        body: JSON.stringify({
            title : title,
            content: content,
            subsector:subsector
        })
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(errorData => {
                throw new Error(errorData.detail || 'Ошибка авторизации');
            });
        }
        return response.json(); // Получаем токены
    })
    .then(data => {
        window.location.href = '/post/'; // Редирект на другую страницу
    })
    .catch(error => {
        // Показываем сообщение об ошибке пользователю
        let errorMessageElement = document.getElementById('error-message');
        errorMessageElement.textContent = error.message;
        errorMessageElement.style.display = 'block';
    });
});

document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".buttons .button").forEach(button => {
        button.addEventListener("click", function () {
            let isLikeButton = this.innerText.trim() === "";
            let countSpan = this.firstChild;
            let currentCount = parseInt(countSpan.textContent);

            if (this.classList.contains("active")) {
                this.classList.remove("active");
                this.style.backgroundColor = ""; // Возвращаем стандартный цвет
                countSpan.textContent = currentCount - 1;
            } else {
                // Убираем активный класс у противоположной кнопки
                let siblingButton = this.parentElement.querySelector(".button.active");
                if (siblingButton) {
                    let siblingCountSpan = siblingButton.firstChild;
                    let siblingCount = parseInt(siblingCountSpan.textContent);
                    siblingButton.classList.remove("active");
                    siblingButton.style.backgroundColor = "";
                    siblingCountSpan.textContent = siblingCount - 1;
                }

                this.classList.add("active");
                this.style.backgroundColor = isLikeButton ? "green" : "red";
                countSpan.textContent = currentCount + 1;
            }
        });
    });
});



//function search() {
//                var input = document.getElementById("searchInput").value;
//                var suggestionsDiv = document.getElementById("suggestions");
//
//                // Очищаем содержимое suggestionsDiv перед каждым новым запросом
//                suggestionsDiv.innerHTML = "";
//
//                // Отправляем запрос на сервер при каждом изменении в поле ввода
//                // Замените URL на URL вашего сервера для обработки запросов
//                fetch("/usersearch/" + input)
//                    .then(response => response.json())
//                    .then(data => {
//                        // Вставляем полученные подходящие варианты в suggestionsDiv
//                        data.forEach(suggestion => {
//                            var suggestionNode = document.createElement("div");
//                            suggestionNode.textContent = suggestion;
//                            suggestionsDiv.appendChild(suggestionNode);
//                        });
//                    })
//                    .catch(error => console.error("Ошибка при отправке запроса:", error));
//            }