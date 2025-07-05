let currentSlide = {};
let images = {};

// Открыть модальное окно для конкретного поста
function openModal(postId, slideIndex) {
    const postContainer = document.querySelector('[data-post-id="' + postId + '"]');

    if (postContainer) {
        images[postId] = postContainer.querySelectorAll('.img-post');
        currentSlide[postId] = slideIndex;

        console.log('Images for post:', images[postId]);

        if (images[postId].length > 0) {
            document.getElementById("imageModal-" + postId).style.display = "flex";
            showSlide(currentSlide[postId], postId);
        } else {
            console.error('No images found for post:', postId);
        }
    } else {
        console.error('Post container not found for post:', postId);
    }
}


// Закрыть модальное окно при клике вне изображения
function closeOnClickOutside(event, postId) {
    if (event.target.classList.contains('modal')) {
        closeModal(postId);
    }
}

// Закрыть модальное окно при нажатии на клавишу Escape
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        let modals = document.querySelectorAll('.modal');
        modals.forEach(modal => {
            modal.style.display = 'none';
        });
    }
});

// Закрыть модальное окно для конкретного поста
function closeModal(postId) {
    document.getElementById("imageModal-" + postId).style.display = "none";
}


// Переключение слайда для конкретного поста
function changeSlide(n, postId) {
    currentSlide[postId] += n;
    if (currentSlide[postId] >= images[postId].length) currentSlide[postId] = 0;
    if (currentSlide[postId] < 0) currentSlide[postId] = images[postId].length - 1;
    showSlide(currentSlide[postId], postId);
}

// Показать текущее изображение для конкретного поста
function showSlide(slideIndex, postId) {
    let modalImg = document.getElementById("modalImg-" + postId);

    if (images[postId][slideIndex]) {
        modalImg.src = images[postId][slideIndex].src;
    } else {
        console.error('Image not found for post:', postId, 'slide:', slideIndex);
    }
}

document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".buttons .button").forEach(button => {
        if (button.id === "reply_comment") return;

        button.addEventListener("click", function () {
            // Получаем контейнер поста или комментария
            let container = this.closest(".container-comment") || this.closest("div[class^='container-']");
            let commentId = container?.dataset.comment || null;
            let postId = container?.dataset.postId || null;

            console.log("Post ID:", postId);
            console.log("Comment ID:", commentId);

            // Тип кнопки (лайк или дизлайк)
            let isLikeButton = this.classList.contains("like-button") || this.dataset.type === "like";
            let type = isLikeButton ? "like" : "dislike";
            console.log("Type:", type);

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

            // Пример: Отправка запроса на бэкенд
            fetch('/reaction/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': '{{ csrf_token }}',
                    'Authorization': `Bearer ${token}`,
                },
                body: JSON.stringify({
                    post: postId,
                    comment: commentId,
                    type: type,
                })
            });

            // Счётчики
            let countSpan = this.firstChild;
            let currentCount = parseInt(countSpan.textContent);

            if (this.classList.contains("active")) {
                this.classList.remove("active");
                this.style.backgroundColor = "";
                countSpan.textContent = currentCount - 1;
            } else {
                let siblingButton = this.parentElement.querySelector(".button.active");
                if (siblingButton && siblingButton.id !== "reply_comment") {
                    let siblingCountSpan = siblingButton.firstChild;
                    let siblingCount = parseInt(siblingCountSpan.textContent);
                    siblingButton.classList.remove("active");
                    siblingButton.style.backgroundColor = "";
                    siblingCountSpan.textContent = siblingCount - 1;
                }

                this.classList.add("active");
                this.style.backgroundColor = isLikeButton ? "rgb(8, 124, 109)" : "rgb(8, 124, 109)";
                countSpan.textContent = currentCount + 1;
            }
        });
    });
});

  const button = document.getElementById('toggleBtn');
  const icon = button.querySelector('i');

  button.addEventListener('click', () => {
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
    // const user = document.querySelector('.user-id').dataset.userId;

    if (icon.classList.contains('fa-user-minus')) {
      icon.classList.remove('fa-user-minus');
      icon.classList.add('fa-user-plus');
      fetch('/unsubscribe/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': '{{ csrf_token }}',
                    'Authorization': `Bearer ${token}`,
                },
                body: JSON.stringify({
                    post: postId,
                    comment: commentId,
                    type: type,
                })
            });
    } else {
      icon.classList.remove('fa-user-plus');
      icon.classList.add('fa-user-minus');
    const userId = document.querySelector('.containerr').dataset.userId;

      fetch('/auth/api/subscribe/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': '{{ csrf_token }}',
                    'Authorization': `Bearer ${token}`,
                },
                body: JSON.stringify({
                    user: userId,
                })
            });
    }
  });