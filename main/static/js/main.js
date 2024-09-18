let currentSlide = {};
let images = {};

// Открыть модальное окно для конкретного поста
function openModal(postId, slideIndex) {
    const postContainer = document.querySelector('[data-post-id="' + postId + '"]');

    if (postContainer) {
        images[postId] = postContainer.querySelectorAll('.img-post');
        currentSlide[postId] = slideIndex;

        console.log('Images for post:', images[postId]);  // Для отладки

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
