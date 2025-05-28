function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken')
const likeButtons = document.querySelectorAll('button[data-question-id]')
console.log(likeButtons)
for (const item of likeButtons)
    item.addEventListener('click', (e) => {
        const value = parseInt(item.dataset.value)
        console.log(item.dataset.value)
        console.log(value)
        const request = new Request(
            `${window.location.origin}/${item.dataset.questionId}/qlike`,
            {
                method: 'POST',
                body: new URLSearchParams({
                   'value' : value
                }),
                headers: {'X-CSRFToken': csrftoken},
                mode: 'same-origin' // Do not send CSRF token to another domain.
            }
        );
        fetch(request).then(response => {
            response.json().then((data) => {
                const counter = document.querySelector(`div[data-question-id="${item.dataset.questionId}"]`)
                counter.innerHTML = data.question_rating
                document.querySelectorAll(`.vote-btn[data-question-id="${item.dataset.questionId}"]`).forEach(b => b.classList.remove('disabled'));

            if (data.user_vote === -1) {
                document.querySelector(`.upvote[data-question-id="${item.dataset.questionId}"]`).classList.add('disabled');
            } else if (data.user_vote === 1) {
                document.querySelector(`.downvote[data-question-id="${item.dataset.questionId}"]`).classList.add('disabled');
            }
            })
        })
    })