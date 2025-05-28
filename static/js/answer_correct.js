document.addEventListener('DOMContentLoaded', () => {
    const question = document.querySelector('a[data-question-id]');
    const questionId = question.dataset.questionId;

    const ansContainer = document.getElementById('ans-container');

    ansContainer.addEventListener('change', function (e) {
        const checkbox = e.target.closest('input[type="checkbox"][data-answer-id]');
        if (!checkbox) return;

        const answerId = checkbox.dataset.answerId;

        const request = new Request(
            `${window.location.origin}/${questionId}/${answerId}/correct`,
            {
                method: 'POST',
                body: new URLSearchParams({}),
                headers: { 'X-CSRFToken': csrftoken },
                mode: 'same-origin'
            }
        );

        fetch(request)
            .then(response => response.json())
            .then(data => {
            })
            .catch(error => console.error("Ошибка при отметке корректного ответа:", error));
    });
});
