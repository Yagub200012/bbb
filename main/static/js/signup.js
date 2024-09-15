document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const username = document.getElementById('username');
    const email = document.getElementById('email');
    const password1 = document.getElementById('password1');
    const password2 = document.getElementById('password2');
    const toggleButtons = document.querySelectorAll('.toggle-password');

    // Проверка паролей и отправка формы
    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Останавливаем стандартное поведение отправки формы

        if (password1.value !== password2.value) {
            // Показываем сообщение об ошибке пользователю
            let errorMessageElement = document.getElementById('error-message');
            errorMessageElement.textContent = 'Пароли не совпадают';
            errorMessageElement.style.display = 'block';
            console.log('видимо не совпали пароли');
        } else {
            // Если пароли совпадают, отправляем данные на сервер
            const formData = {
                username: username.value,
                email: email.value,
                password: password1.value,
                confirm_password: password2.value,
            };

            fetch('/auth/api/register/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value // Берем CSRF токен
                },
                body: JSON.stringify(formData)
            })
            .then(response => {
                if (!response.ok) {
                    console.log('Ответ сервера не ок');
                    return response.json().then(errorData => {
                        throw new Error(errorData.detail || 'Ошибка регистрации');
                    });
                }
                console.log('Получен ответ сервера');
                return response.json(); // Получаем токены
            })
            .then(data => {
                window.location.href = '/auth/login/';
            })
            .catch(error => {
                // Показываем сообщение об ошибке пользователю
                let errorMessageElement = document.getElementById('error-message');
                errorMessageElement.textContent = error.message;
                errorMessageElement.style.display = 'block';
                console.log('Ошибка:', error.message);
            });
        }
    });

    // Управление видимостью паролей
    toggleButtons.forEach(button => {
        button.addEventListener('click', function() {
            const input = this.previousElementSibling;
            if (input.type === 'password') {
                input.type = 'text';
                this.textContent = '😐'; // Меняем иконку
            } else {
                input.type = 'password';
                this.textContent = '😑'; // Меняем иконку обратно
            }
        });
    });
});
