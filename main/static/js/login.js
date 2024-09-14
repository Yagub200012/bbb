document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Остановить стандартную отправку формы

    let username = document.getElementById('username').value;
    let password = document.getElementById('password').value;

    // Отправляем запрос на API
    fetch('/auth/api/token/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}' // Если нужно передать CSRF токен
        },
        body: JSON.stringify({
            username: username,
            password: password
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
        // Сохраняем токены в куки
        document.cookie = `accessToken=${data.access}; path=/; secure`;
        document.cookie = `refreshToken=${data.refresh}; path=/; secure`;
        console.log('Токены сохранены в куки', data);

        // Пример: Перенаправление после успешной авторизации
        window.location.href = '/auth/profile/'; // Редирект на другую страницу
    })
    .catch(error => {
        // Показываем сообщение об ошибке пользователю
        let errorMessageElement = document.getElementById('error-message');
        errorMessageElement.textContent = error.message;
        errorMessageElement.style.display = 'block';
    });
});
