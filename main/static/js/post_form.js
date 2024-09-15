document.getElementById('PostForm').addEventListener('submit', async function(event) {
    event.preventDefault();  // Останавливаем стандартное поведение формы

    const form = document.getElementById('PostForm');
    const formData = new FormData(form);

    // Функция для извлечения JWT токена из куки
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Проверяем, начинается ли cookie с искомого имени
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const token = getCookie('accessToken');  // Название куки, где хранится токен

    // Отправляем данные на API
    try {
        const response = await fetch('/api/post_create/', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                // Не указываем 'Content-Type', так как FormData сам добавит нужный заголовок
            },
            body: formData
        });

        if (response.ok) {
            // Если запрос успешный, перенаправляем на главную страницу
            window.location.href = '';
        } else {
            const errorData = await response.json();
            console.error('Ошибка при отправке данных:', errorData);
            alert('Ошибка при создании задания');
        }
    } catch (error) {
        console.error('Произошла ошибка:', error);
        alert('Произошла ошибка при соединении с сервером');
    }
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

