
let offset = 15;
let isLoading = false;
let hasMore = true;

let comment_input = document.getElementById('comment');

document.getElementById('CommentForm').addEventListener('submit', async function(event) {
    event.preventDefault();  // Останавливаем стандартное поведение формы

    let replyInput = document.getElementById('content');

    if (replyInput.value) {

        const form = document.getElementById('CommentForm');
        const formData = new FormData(form);
//        for (let [key, value] of formData.entries()) {
//            console.log(`${key}:`, value);
//        }


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
            const response = await fetch('/api/comment_create/', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    // Не указываем 'Content-Type', так как FormData сам добавит нужный заголовок
                },
                body: formData
            });

            const quoteBox = document.querySelector('.container-quote');
            if (quoteBox) quoteBox.remove();


            let lastComment = document.querySelector('.coms .container-comment:last-child');

            const data = await response.json();
            renderComment(data);

            comment_input.value = null;


            if (response.ok) {
                    // Очищаем textarea после успешной отправки
                    document.getElementById('content').value = '';
                    // Также можно очистить скрытые поля, если нужно:
                    document.getElementById('replied_to').value = '';
                    document.getElementById('comment').value = '';
                    // Удаляем цитату, если есть

                    let lastComment = document.querySelector('.coms .container-comment:last-child');
                    let lastId = lastComment ? lastComment.dataset.comment : null;
                    offset = lastId
                    console.log(offset);

            } else {
                const errorData = await response.json();
//                console.log('форма:',formData);
//                console.error('Ошибка при отправке данных:', errorData);
//                alert('Ошибка при создании задания');
            }
        } catch (error) {
//            console.error('Произошла ошибка:', error);
//            alert('Произошла ошибка при соединении с сервером');
        }
    }
});


document.addEventListener('click', function(event) {
    if (event.target.matches('.button#reply_comment')) {
        let commentContainer = event.target.closest('.container-comment');
//        let user = commentContainer.getAttribute('data-user');
        let comment = commentContainer.getAttribute('data-comment');
        let commenttext = commentContainer.getAttribute('data-commenttext');

        let replyInput = document.getElementById('content');

        if (comment) {
            let commentBox = document.querySelector('.container-quote');
            let username = commentContainer.getAttribute('data-username');
//            let replied_to_input = document.getElementById('replied_to');
//            let comment_input = document.getElementById('comment');

            comment_input.value = comment;
//            replied_to_input.value = user;

            if (commentBox) {
                commentBox.innerHTML = `${username}: ${commenttext} <span class="close-btn" style="cursor: pointer; margin-left: 10px;">&times;</span>`;
            } else {
                document.getElementById('CommentForm').insertAdjacentHTML(
                    "afterbegin",
                    `<div class="container-quote">
                    ${username}: ${commenttext}
                    <span class="close-btn">&times;</span>
                    </div>`
                );
            }

            document.querySelector('.close-btn').addEventListener("click", function () {
                document.querySelector('.container-quote').remove();
                comment_input.value = null;
//                replied_to_input.value = null;
            });

            replyInput.focus();
        }
    }
});


document.addEventListener("DOMContentLoaded", function () {
    // Используем делегирование событий для кнопок лайка/дизлайка
    document.addEventListener("click", function (event) {
        // Проверяем, что клик был по кнопке лайка или дизлайка, но не по reply_comment
        if (
            event.target.closest(".buttons .button") &&
            event.target.closest(".button").id !== "reply_comment"
        ) {
            let button = event.target.closest(".button");
            // Получаем контейнер поста или комментария
            let container = button.closest(".container-comment") || button.closest("div[class^='container-']");
            let commentId = container?.dataset.comment || null;
            let postId = container?.dataset.postId || null;

            // Тип кнопки (лайк или дизлайк)
            let isLikeButton = button.classList.contains("like-button") || button.dataset.type === "like";
            let type = isLikeButton ? "like" : "dislike";

            // Функция для извлечения JWT токена из куки
            function getCookie(name) {
                let cookieValue = null;
                if (document.cookie && document.cookie !== '') {
                    const cookies = document.cookie.split(';');
                    for (let i = 0; i < cookies.length; i++) {
                        const cookie = cookies[i].trim();
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
            let countSpan = button.firstChild;
            let currentCount = parseInt(countSpan.textContent);

            if (button.classList.contains("active")) {
                button.classList.remove("active");
                button.style.backgroundColor = "";
                countSpan.textContent = currentCount - 1;
            } else {
                let siblingButton = button.parentElement.querySelector(".button.active");
                if (siblingButton && siblingButton.id !== "reply_comment") {
                    let siblingCountSpan = siblingButton.firstChild;
                    let siblingCount = parseInt(siblingCountSpan.textContent);
                    siblingButton.classList.remove("active");
                    siblingButton.style.backgroundColor = "";
                    siblingCountSpan.textContent = siblingCount - 1;
                }

                button.classList.add("active");
                button.style.backgroundColor = isLikeButton ? "rgb(8, 124, 109)" : "rgb(8, 124, 109)";
                countSpan.textContent = currentCount + 1;
            }
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







window.addEventListener('scroll', () => {
    if (!isLoading && hasMore && (window.innerHeight + window.scrollY >= document.body.offsetHeight - 300)) {
        loadMore();
    }
});
function loadMore() {
    isLoading = true;
    document.getElementById('loader').style.display = 'block';

    function getCookie(name) {
                let cookieValue = null;
                if (document.cookie && document.cookie !== '') {
                    const cookies = document.cookie.split(';');
                    for (let i = 0; i < cookies.length; i++) {
                        const cookie = cookies[i].trim();
                        if (cookie.substring(0, name.length + 1) === (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }
            const token = getCookie('accessToken');


    // Получаем postId из глобального контекста или из DOM, если нужно
    let postId = null;
    const postContainer = document.querySelector(".container-post") || document.querySelector("div[data-post-id]");
    if (postContainer) {
        postId = postContainer.dataset.postId || postContainer.getAttribute("data-post-id");
    }

    fetch(`/api/load-comments/?offset=${offset}&limit=10&post=${postId}`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`
        }})
        .then(res => res.json())
        .then(data => {
//            document.getElementById('loader').style.display = 'none';
            if (data.length === 0) {
                hasMore = false;
                return;
            }

            offset += data.length;

            data.forEach(comment => {
                renderComment(comment);
            });

//            data.forEach(comment => {
//                console.log("Комментарий:");
//                for (const [key, value] of Object.entries(comment)) {
//                    console.log(`${key}:`, value);
//                }
//            });


            isLoading = false;
        })
        .catch(err => {
            console.error("Ошибка загрузки уведомлений:", err);
            isLoading = false;
//            document.getElementById('loader').style.display = 'none';
        });
}


function renderComment(comment) {
    const content = document.querySelector('.coms');
    const div = document.createElement('div');
    div.classList.add('container-comment');
    div.dataset.user = comment.user.id;
    div.dataset.comment = comment.id;
    div.dataset.commenttext = comment.text.slice(0, 30);
    div.dataset.username = comment.user.username;

    const date = new Date(comment.created_at);
    const formattedDate = date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) + ' ' +
        date.toLocaleDateString('ru-RU');

    const avatar = comment.user.avatar
        ? `https://i.imgur.com/${comment.user.avatar}`
        : '/static/images/def_log.jpg';

    const markIcon = comment.user.mark ? `
        <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" viewBox="0 0 200 200" class="small-icon-posts">
            <circle cx="100" cy="100" r="100" style="fill:${comment.user.mark};stroke-width:0.45914;fill-opacity:1"/>
            <path style="fill:#ffffff;stroke-width:0.593542;fill-opacity:1"
                d="M 21.332094,72.362596 53.252163,144.64266 178.05812,81.98334 171.3519,67.92009 61.334205,123.28926 36.123514,66.606266 Z"/>
        </svg>` : '';

    const repliedQuote = (comment.comment_inst)
        ? `<div class="container-quote-Random">${comment.replied_to.username}: ${comment.comment_inst.text.slice(0, 30)}</div>`
        : '';

    const likeBtnClass = comment.reaction?.[0]?.type === 'like' ? 'button active' : 'button';
    const dislikeBtnClass = comment.reaction?.[0]?.type === 'dislike' ? 'button active' : 'button';

    const likeStyle = comment.reaction?.[0]?.type === 'like' ? 'style="background-color: rgb(8, 124, 109);"' : '';
    const dislikeStyle = comment.reaction?.[0]?.type === 'dislike' ? 'style="background-color: rgb(8, 124, 109);"' : '';
//
//    let reply = ""
//
//    if (comment.comment) {
//        let reply = `
//            <div class="container-quote-Random">
//                ${comment.replied_to.username}: ${comment.comment.text}
//            </div>
//        `
//    }

    div.innerHTML = `
        <div class="header">
            <a href="/auth/profile/${comment.user.id}" class="button-sector">
                <div class="avatar-and-nick">
                    <img src="${avatar}" alt="Avatar">
                    <span class="nick">${comment.user.username}</span>
                    ${markIcon}
                </div>
            </a>
            <span class="small-text">${formattedDate}</span>
        </div>
        ${repliedQuote}
        <p>${comment.text}</p>
        <div class="buttons">
            <button class=${likeBtnClass} ${likeStyle} data-type="like">${comment.likes}
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20">
                    <polygon points="10,5 15,15 5,15" fill="white"/>
                </svg>
            </button>

            <button class=${dislikeBtnClass} id="dislike-button" ${dislikeStyle}>${comment.dislikes}
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20">
                    <polygon points="5,5 15,5 10,15" fill="white"/>
                </svg>
            </button>

            <button class="button" id="reply_comment">
                ответить
            </button>
        </div>
    `;

    content.appendChild(div);
}











//let loading = false;
//let lastCommentId = 0;
//let oldestCommentId = null;
//
//function loadMoreComments(direction = 'down') {
//    if (loading) return;
//    loading = true;
//
//    const fromId = direction === 'down' ? lastCommentId : oldestCommentId;
//
//    fetch(`/get_comments/${postId}/?from_id=${fromId}&direction=${direction}`)
//        .then(r => r.json())
//        .then(data => {
//            const container = document.getElementById('comments-container');
//            if (data.comments.length === 0) return;
//
//            data.comments.forEach(comment => {
//                const el = document.createElement('div');
//                el.className = 'comment';
//                el.textContent = `${comment.author}: ${comment.text}`;
//                if (direction === 'down') container.appendChild(el);
//                else container.prepend(el);
//                lastCommentId = Math.max(lastCommentId, comment.id);
//                oldestCommentId = oldestCommentId === null ? comment.id : Math.min(oldestCommentId, comment.id);
//            });
//        })
//        .finally(() => loading = false);
//}
//
//
//document.addEventListener('DOMContentLoaded', () => {
//    loadMoreComments();  // initial load
//
//    const container = document.getElementById('comments-container');
//
//    container.addEventListener('scroll', () => {
//        const nearBottom = container.scrollTop + container.clientHeight >= container.scrollHeight - 100;
//        const nearTop = container.scrollTop <= 100;
//
//        if (nearBottom) loadMoreComments('down');
//        if (nearTop) loadMoreComments('up');
//    });
//
//    document.getElementById('scroll-to-bottom').addEventListener('click', () => {
//        fetch(`/get_last_comment_id/${postId}/`)
//            .then(r => r.json())
//            .then(data => {
//                lastCommentId = data.last_id;
//                document.getElementById('comments-container').innerHTML = '';
//                loadMoreComments('up');
//                setTimeout(() => {
//                    container.scrollTop = container.scrollHeight;
//                }, 300);
//            });
//    });
//});
