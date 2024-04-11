async function filterGames() {
    const form = document.getElementById('gameFilterForm');
    const formData = new FormData(form);
    let duration = formData.get('duration');
    let location = formData.get('location');
    let theme = formData.get('theme');

    // Если выбран первый пункт списка, устанавливаем пустую строку
    duration = (duration === "Выберите продолжительность") ? "" : duration;
    location = (location === "Выберите место проведения") ? "" : location;
    theme = (theme === "Выберите тему") ? "" : theme;

    const gamesList = document.getElementById('gamesList');
    gamesList.innerHTML = ''; // Очистка предыдущего списка игр

    try {
        const response = await fetch('/get_games_data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                duration: duration,
                location: location,
                theme: theme
            })
        });

        if (!response.ok) {
            throw new Error('Ошибка получения данных');
        }

        const gamesData = await response.json();
        gamesData.forEach(game => {
            const gameDiv = document.createElement('div');
            gameDiv.classList.add('game');

            // Создаем элементы для отображения информации о задаче
            const titleHeader = document.createElement('h2');
            titleHeader.textContent = game.title;
            gameDiv.appendChild(titleHeader);

            const durationPara = document.createElement('p');
            durationPara.textContent = `Продолжительность: ${game.duration}`;
            gameDiv.appendChild(durationPara);

            const locationPara = document.createElement('p');
            locationPara.textContent = `Место проведения: ${game.location}`;
            gameDiv.appendChild(locationPara);

            const themePara = document.createElement('p');
            themePara.textContent = `Тема: ${game.theme}`;
            gameDiv.appendChild(themePara);

            const conditionPara = document.createElement('p');
            conditionPara.textContent = `Условие: ${game.condition}`;
            gameDiv.appendChild(conditionPara);

            gamesList.appendChild(gameDiv);
        });
    } catch (error) {
        console.error('Ошибка при получении данных:', error);
    }
}