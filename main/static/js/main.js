let currentSlide = {};
let images = {};

function openModal(postId, slideIndex) {
    const postContainer = document.querySelector('[data-post-id="' + postId + '"]');

    if (postContainer) {
        images[postId] = postContainer.querySelectorAll('.img-post');
        currentSlide[postId] = slideIndex;

        if (images[postId].length > 0) {
            document.getElementById("imageModal-" + postId).style.display = "flex";
            showSlide(currentSlide[postId], postId);
        }
    }
}

function closeOnClickOutside(event, postId) {
    if (event.target.classList.contains('modal')) {
        closeModal(postId);
    }
}

document.addEventListener('keydown', function (event) {
    if (event.key === 'Escape') {
        let modals = document.querySelectorAll('.modal');
        modals.forEach(modal => {
            modal.style.display = 'none';
        });
    }
});

function closeModal(postId) {
    document.getElementById("imageModal-" + postId).style.display = "none";
}

function changeSlide(n, postId) {
    currentSlide[postId] += n;
    if (currentSlide[postId] >= images[postId].length) currentSlide[postId] = 0;
    if (currentSlide[postId] < 0) currentSlide[postId] = images[postId].length - 1;
    showSlide(currentSlide[postId], postId);
}

function showSlide(slideIndex, postId) {
    let modalImg = document.getElementById("modalImg-" + postId);

    if (images[postId][slideIndex]) {
        modalImg.src = images[postId][slideIndex].src;
    }
}

document.addEventListener("DOMContentLoaded", function () {
    attachReactionListeners(document);
});

function attachReactionListeners(container) {
    container.querySelectorAll(".buttons .button").forEach(button => {
        if (button.id === "reply_comment") return;

        button.addEventListener("click", function () {
            let parent = this.closest(".container-comment") || this.closest("div[class^='container-']");
            let commentId = parent?.dataset.comment || null;
            let postId = parent?.dataset.postId || null;

            let isLikeButton = this.classList.contains("like-button") || this.dataset.type === "like";
            let type = isLikeButton ? "like" : "dislike";

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
                this.style.backgroundColor = "rgb(8, 124, 109)";
                countSpan.textContent = currentCount + 1;
            }
        });
    });
}

let offset = 10;
let isLoading = false;
let hasMore = true;

window.addEventListener('scroll', () => {
    if (!isLoading && hasMore && (window.innerHeight + window.scrollY >= document.body.offsetHeight - 300)) {
        loadMore();
    }
});

const h1 = document.querySelector('h1[data-subsector-id]');
const subsectorId = h1 ? `&subsector=${h1.getAttribute('data-subsector-id')}` : '';

const h11 = document.querySelector('h1[data-sector-id]');
const sectorId = h11 ? `&sector=${h11.getAttribute('data-sector-id')}` : '';

function loadMore() {
    isLoading = true;
    document.getElementById('loader').style.display = 'block';

    fetch(`/api/load-posts/?offset=${offset}&limit=10${subsectorId}${sectorId}`)
        .then(res => res.json())
        .then(data => {
//            document.getElementById('loader').style.display = 'none';
            if (data.length === 0) {
                hasMore = false;
                return;
            }

            offset += data.length;

            data.forEach(post => {
                renderPost(post);
            });

            isLoading = false;
        })
        .catch(err => {
            console.error("Ошибка загрузки постов:", err);
            isLoading = false;
//            document.getElementById('loader').style.display = 'none';
        });
}


function renderPost(post) {
    const container = document.querySelector('.mainpage_container');
    const div = document.createElement('div');
    div.className = `container-${post.subsector.sector.title}`;
    div.setAttribute('data-post-id', post.id);

    const userMarkSVG = post.user.mark ? `
        <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" viewBox="0 0 200 200" class="small-icon-posts">
            <circle cx="100" cy="100" r="100" style="fill:${post.user.mark};stroke-width:0.45914;fill-opacity:1" />
            <path style="fill:#ffffff;stroke-width:0.593542;fill-opacity:1"
                d="M 21.332094,72.362596 53.252163,144.64266 178.05812,81.98334 171.3519,67.92009 61.334205,123.28926 36.123514,66.606266 Z" />
        </svg>` : '';

    const createdAt = new Date(post.created_at);
    const formattedDate = createdAt.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) + ' ' +
        createdAt.toLocaleDateString('ru-RU');

    const truncated = post.content && post.content.length > 400;
    const content = post.content
        ? (truncated ? post.content.slice(0, 400) + ` <span class="small-text"><a href="/post/${post.id}" style="color:#ffffff2a">читать далее...</a></span>` : post.content)
        : '';

    const images = post.images
        .map((img, i) => `<img class="img-post" src="https://i.imgur.com/${img.image_link}" onclick="openModal(${post.id}, ${i})">`)
        .join('');



    const modal = `
        <div id="imageModal-${post.id}" class="modal" onclick="closeOnClickOutside(event, ${post.id})">
            <span class="close" onclick="closeModal(${post.id})">&times;</span>
            <div class="modal-content">
                <button class="prev" onclick="changeSlide(-1, ${post.id})">&#10094;</button>
                <img class="modal-img" id="modalImg-${post.id}" onclick="changeSlide(1, ${post.id})">
                <button class="next" onclick="changeSlide(1, ${post.id})">&#10095;</button>
            </div>
        </div>
    `;

    const likeBtnClass = post.reaction?.[0]?.type === 'like' ? 'button active' : 'button';
    const dislikeBtnClass = post.reaction?.[0]?.type === 'dislike' ? 'button active' : 'button';

    const likeStyle = post.reaction?.[0]?.type === 'like' ? 'style="background-color: rgb(8, 124, 109);"' : '';
    const dislikeStyle = post.reaction?.[0]?.type === 'dislike' ? 'style="background-color: rgb(8, 124, 109);"' : '';

    div.innerHTML = `
        <div class="header">
            <a href="/auth/profile/${post.user.id}" class="button-sector">
                <div class="avatar-and-nick">
                    <img src="https://i.imgur.com/${post.user.avatar}" alt="Avatar">
                    <span class="nick">${post.user.username}</span>
                    ${userMarkSVG}
                </div>
            </a>
            <span class="small-text">${formattedDate}</span>
        </div>

        <h2>${post.title}</h2>

        ${content ? `<p>${content}</p><br>` : ''}

        <a href="/subsector_post/?subsector_id=${post.subsector.id}">
            <span class="small-text-${post.subsector.sector.title}">/${post.subsector.sector.title}/${post.subsector.title}/</span>
        </a>
        <br><br>

        <div class="im-container" data-post-id="${post.id}">
            ${images}
        </div>

        ${modal}

        <br>

        <div class="buttons">
            <button class="${likeBtnClass}" ${likeStyle} data-type="like">${post.likes}
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20">
                    <polygon points="10,5 15,15 5,15" fill="white"/>
                </svg>
            </button>

            <button class="${dislikeBtnClass}" ${dislikeStyle}>${post.dislikes}
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20">
                    <polygon points="5,5 15,5 10,15" fill="white"/>
                </svg>
            </button>

            <button class="button" id="reply_comment" onclick="window.location.href='/post/${post.id}';">
                ${post.comments}
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="15" viewBox="0 0 20 20">
                    <path d="M1 2h18a1 1 0 0 1 1 1v14a1 1 0 0 1-1 1H5l-4 4V3a1 1 0 0 1 1-1z" fill="white"/>
                </svg>
            </button>
        </div>
    `;

    container.appendChild(div);
    attachReactionListeners(div);
}















const mobileMenu = document.getElementById('mobileMenu');
let lastMenuScrollY = window.scrollY;
let lastMenuState = 'shown';

window.addEventListener('scroll', () => {
    const currentScrollY = window.scrollY;

    if (currentScrollY === 0) {
        // На самом верху страницы — скрываем меню
        mobileMenu.style.transform = 'translateY(-100%)';
        mobileMenu.style.opacity = '0';
        mobileMenu.style.pointerEvents = 'none';
        lastMenuState = 'hidden';
    } else if (currentScrollY < lastMenuScrollY) {
        // Скролл вверх — показываем меню
        if (lastMenuState !== 'shown') {
            mobileMenu.style.transform = 'translateY(0)';
            mobileMenu.style.opacity = '1';
            mobileMenu.style.pointerEvents = 'auto';
            lastMenuState = 'shown';
        }
    } else if (currentScrollY > lastMenuScrollY) {
        // Скролл вниз — скрываем меню
        if (lastMenuState !== 'hidden') {
            mobileMenu.style.transform = 'translateY(-100%)';
            mobileMenu.style.opacity = '0';
            mobileMenu.style.pointerEvents = 'none';
            lastMenuState = 'hidden';
        }
    }
    lastMenuScrollY = currentScrollY;
});







document.addEventListener('DOMContentLoaded', () => {
  const menu = document.getElementById('mobileMenu');
  const submenu = document.getElementById('submenu');
  const content = document.body;
  let openTopic = null;

  window.addEventListener('scroll', () => {
  submenu.classList.remove('visible');
  content.classList.remove('blur');
  openTopic = null;
});

  // Обработка кликов по меню
  menu.addEventListener('click', e => {
    const topic = e.target.dataset.topic;
    if (!topic) return;

    if (openTopic === topic) {
      const firstLink = submenu.querySelector(`.topic-submenu[data-topic="${topic}"] a`);
      if (firstLink) window.location = firstLink.href;
      return;
    }

    submenu.querySelectorAll('.topic-submenu').forEach(div => {
      div.style.display = div.dataset.topic === topic ? 'block' : 'none';
    });

    submenu.classList.add('visible');
    content.classList.add('blur');
    openTopic = topic;
  });

  // Закрытие по клику вне меню
  document.addEventListener('click', e => {
    if (!menu.contains(e.target) && !submenu.contains(e.target)) {
      submenu.classList.remove('visible');
      content.classList.remove('blur');
      openTopic = null;
    }
  });

  // Скролл — сворачивать блоки
  document.addEventListener('scroll', () => {
    const blocks = document.querySelectorAll('.sector-block');
    if (window.scrollY > 100) {
      blocks.forEach(b => b.classList.add('collapsed'));
    } else {
      blocks.forEach(b => b.classList.remove('collapsed'));
    }
  });
});
