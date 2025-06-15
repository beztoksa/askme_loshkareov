document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("search-box");
    const list = document.getElementById("suggestions-list");
    let currentFocus = -1;
    let suggestionsData = [];
    list.style.position = 'absolute';
    list.style.zIndex = '9999';
    list.style.display = 'none';


    function debounce(func, delay) {
        let timer;
        return function(...args) {
            clearTimeout(timer);
            timer = setTimeout(() => func.apply(this, args), delay);
        };
    }

    const fetchSuggestions = () => {
        const q = input.value.trim();

        if (q.length < 2) {
            list.style.display = "none";
            return;
        }

        fetch(`${window.location.origin}/search_suggestions/?q=${encodeURIComponent(q)}`)
            .then(res => res.json())
            .then(data => {
                list.innerHTML = '';
                suggestionsData = data.suggestions || [];

                if (suggestionsData.length === 0) {
                    list.style.display = "none";
                    return;
                }

                suggestionsData.forEach((item, index) => {
                    const li = document.createElement('li');
                    li.textContent = item.title;
                    li.dataset.id = item.id;
                    li.style.cursor = 'pointer';
                    li.style.padding = '8px';
                    li.classList.add('suggestion-item');

                    li.addEventListener('click', () => {
                        selectItem(item);
                        input.form.submit();
                    });

                    li.addEventListener('mouseover', () => {
                        currentFocus = index;
                        setActiveItems();
                    });

                    list.appendChild(li);
                });

                list.style.display = 'block';
                currentFocus = -1;
            });
    };

    function setActiveItems() {
        const items = list.querySelectorAll('.suggestion-item');
        items.forEach((item, index) => {
            item.classList.toggle('active', index === currentFocus);
            if (index === currentFocus) {
                item.scrollIntoView({
                    block: 'nearest',
                    behavior: 'smooth'
                });
            }
        });
    }

    function selectItem(item) {
        input.value = item.title;
        list.style.display = 'none';
        currentFocus = -1;
    }

    input.addEventListener("input", debounce(fetchSuggestions, 300));

input.addEventListener('keydown', function(e) {
        const items = list.querySelectorAll('li');
        if (!items.length) return;

        if (e.key === 'ArrowDown') {
            currentFocus = (currentFocus + 1) % items.length;
        } else if (e.key === 'ArrowUp') {
            currentFocus = (currentFocus - 1 + items.length) % items.length;
        } else return;

        items.forEach((item, i) => {
            item.style.backgroundColor = i === currentFocus ? '#e0e0e0' : '';
        });

        items[currentFocus].scrollIntoView({ block: 'nearest' });
    });
    document.addEventListener('click', function(e) {
        if (e.target !== input && !list.contains(e.target)) {
            list.style.display = 'none';
        }
    });
});