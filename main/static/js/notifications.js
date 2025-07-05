let offset = 15;
let isLoading = false;
let hasMore = true;

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

    fetch(`/notifications/api/load_notifications/?offset=${offset}&limit=10`, {
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

            data.forEach(notif => {
                renderNotif(notif);
            });

            isLoading = false;
        })
        .catch(err => {
            console.error("Ошибка загрузки уведомлений:", err);
            isLoading = false;
//            document.getElementById('loader').style.display = 'none';
        });
}


function renderNotif(notif) {
    const notifs = document.querySelector('.notifs');
    const a = document.createElement('a');
    a.setAttribute('href', `/post/${notif.post}`);
    a.setAttribute('class', "button-sector");
    console.log(notif.type)

    let clas = ""

    if (notif.type == 'reply') {
    clas = "fa-reply"
    } else if (notif.type == 'comment') {
    clas = "fa-comment"
    } else if (notif.type == 'p_like') {
    clas = "fa-thumbs-up"
    } else if (notif.type == 'c_like') {
    clas = "fa-thumbs-up"}
    console.log(clas)

    const date = new Date(notif.event_date);
    const formattedDate = date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) + ' ' +
        date.toLocaleDateString('ru-RU');

    a.innerHTML = `
        <div class="container-comment">
            <div class="header">
                <div class="avatar-and-nick">
                    <span class="nick">
                        <i class="fa-solid ${clas}" style="color:orange"></i>
                    &nbsp;${notif.description}</span>
                </div>
                <span class="small-text">${formattedDate}</span>
            </div>
        </div>
    `;

    notifs.appendChild(a);
}
