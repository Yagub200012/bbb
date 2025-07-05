document.getElementById('PostForm').addEventListener('submit', async function(event) {
    event.preventDefault();  // Останавливаем стандартное поведение формы

    const form = document.getElementById('PostForm');
    const formData = new FormData(form);
    console.log(formData.get('photo'));
    console.log(formData.get('username'));
    console.log(formData.get('bio'));

//    const photoFile = formData.get('photo'); // Получаем файл из FormData

    if (formData.get('photo').size === 0) {
      formData.delete('photo'); // Удаляем поле, если файла нет или он пустой
    }


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
    let user_id = document.getElementById('pk').value;
    // Отправляем данные на API
    try {
        const response = await fetch('/auth/api/update/' + user_id, {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${token}`,
                // Не указываем 'Content-Type', так как FormData сам добавит нужный заголовок
            },
            body: formData
        });

        if (response.ok) {
            // Если запрос успешный, перенаправляем на главную страницу
            window.location.href = '/auth/profile/0';
        } else {
            const errorData = await response.json();
            console.error('Ошибка при отправке данных:', errorData);
            let errorMessageElement = document.getElementById('error-message');
            errorMessageElement.textContent = error.message;
            errorMessageElement.style.display = 'block';
            console.log('Ошибка:', error.message);
        }
    } catch (error) {
        console.error('Произошла ошибка:', error);
        let errorMessageElement = document.getElementById('error-message');
                errorMessageElement.textContent = error.message;
                errorMessageElement.style.display = 'block';
                console.log('Ошибка:', error.message);
    }
});

document.querySelectorAll('.image-input').forEach(input => {
    input.addEventListener('change', function () {
        const previewId = 'preview' + this.id.slice(-1);
        const preview = document.getElementById(previewId);

        const file = this.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function (e) {
                preview.src = e.target.result;
                preview.style.display = 'block';
                preview.previousElementSibling.style.display = 'none'; // скрываем плюсик
            };
            reader.readAsDataURL(file);
        }
    });
});
