document.getElementById('PostForm').addEventListener('submit', async function(event) {
    event.preventDefault();  // Останавливаем стандартное поведение формы

    const form = document.getElementById('PostForm');
    const formData = new FormData(form);
        for (const [key, value] of formData.entries()) {
          console.log(key, value);
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
            window.location.href = '/';
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

const textarea = document.getElementById('content');
const lineHeight = 20; // высота одной строки — подстрой под свой стиль

// Устанавливаем начальную высоту (например, одна строка)
textarea.style.height = lineHeight + 'px';

textarea.addEventListener('input', function () {
  this.style.height = lineHeight + 'px'; // сброс до одной строки

  // Вычисляем количество строк
  const lines = Math.floor(this.scrollHeight / lineHeight);

  // Устанавливаем высоту по числу строк
  this.style.height = (lines * lineHeight) + 'px';
});

// Триггерим при загрузке (если есть текст)
textarea.dispatchEvent(new Event('input'));

//const maxHeight = 150;
//this.style.height = Math.min(this.scrollHeight, maxHeight) + 'px';

//----------------------------------------------------------------------------------------------------------------------
//<input type="file" id="imageInput" multiple>
//<button onclick="handleMultiUpload()">Upload All</button>
//
//<script>
//  async function uploadToTelegraph(files) {
//    const formData = new FormData();
//    for (let file of files) {
//      formData.append('file', file);
//    }
//
//    const response = await fetch('https://telegra.ph/upload', {
//      method: 'POST',
//      body: formData
//    });
//
//    const result = await response.json();
//
//    if (result.error) {
//      throw new Error(result.error);
//    }
//
//    // Массив прямых ссылок
//    return result.map(item => 'https://telegra.ph' + item.src);
//  }
//
//  async function handleMultiUpload() {
//    const input = document.getElementById('imageInput');
//    const files = input.files;
//    if (files.length === 0) return alert("Выберите хотя бы один файл");
//
//    try {
//      const urls = await uploadToTelegraph(files);
//      console.log('Ссылки на изображения:', urls);
//      alert('Загружено:\n' + urls.join('\n'));
//    } catch (err) {
//      console.error(err);
//      alert('Ошибка: ' + err.message);
//    }
//  }
//</script>
