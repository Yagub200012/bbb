document.querySelectorAll('.myLink').forEach(function(link) {
        link.addEventListener('click', function(event) {
            event.preventDefault(); // Остановить стандартное действие по переходу по ссылке

            const accessToken = getCookie('access_token'); // Получаем токен с помощью js-cookie

            if (!accessToken) {
                alert('Токен не найден');
                return;
            }

            fetch(link.href, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${accessToken}`
                }
            })
            .then(response => response.json())
            .then(data => {
                console.log(data);
                window.location.href = link.href; // Переход на страницу после успешного запроса
            })
            .catch(error => console.error('Ошибка:', error));
        });
    });

    // Функция для получения значения куки по имени
    function getCookie(name) {
        let matches = document.cookie.match(new RegExp(
            "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
        ));
        return matches ? decodeURIComponent(matches[1]) : undefined;
    }