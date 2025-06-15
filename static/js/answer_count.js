document.getElementById('ans-container').addEventListener('click', function (e) {
    const button = e.target.closest('button.vote-btn[data-answer-id]');
    if (!button) return;  // не лайк-кнопка — выходим        const button = e.currentTarget;
    const value = parseInt(button.dataset.value);
    const id = button.dataset.answerId;
    console.log(button.dataset.value)
    console.log(value)
    const request = new Request(
        `${window.location.origin}/${id}/alike`,
        {
            method: 'POST',
            body: new URLSearchParams({
                'value': value
            }),
            headers: {'X-CSRFToken': csrftoken},
            mode: 'same-origin' // Do not send CSRF token to another domain.
        }
    );
    fetch(request)
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => {
                    throw new Error(err.error || 'Произошла ошибка');
                });
            }

            return response.json();
        })
        .then((data) => {
            const counter = document.querySelector(`div[data-answer-id="${id}"]`)
            counter.innerHTML = data.answer_rating
            document.querySelectorAll(`.vote-btn[data-answer-id="${id}"]`).forEach(b => b.classList.remove('disabled'));

            if (data.user_vote === -1) {
                document.querySelector(`.upvote[data-answer-id="${id}"]`).classList.add('disabled');
            } else if (data.user_vote === 1) {
                document.querySelector(`.downvote[data-answer-id="${id}"]`).classList.add('disabled');
            }
        })
})