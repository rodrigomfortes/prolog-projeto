document.getElementById('genre-form').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const genres = Array.from(document.querySelectorAll('input[name="genre"]:checked'))
                         .map(input => input.value);
    
    if (genres.length === 0) {
        alert("Por favor, selecione pelo menos um gênero.");
        return;
    }
    
    fetchRecommendations(genres);
});

function fetchRecommendations(genres) {
    const query = genres.join(',');
    
    fetch(`/recommend?genres=${query}`)
        .then(response => response.json())
        .then(data => {
            displayRecommendations(data);
        })
        .catch(error => console.error('Erro na recomendação:', error));
}

function displayRecommendations(recommendations) {
    const list = document.getElementById('movie-recommendations');
    list.innerHTML = ''; // Limpa a lista atual
    
    recommendations.forEach(movie => {
        const listItem = document.createElement('li');
        listItem.innerHTML = `
            <img src="${movie.image}" alt="${movie.title}">
            <strong>${movie.title}</strong> (Nota: ${movie.rating})
            <button onclick="markAsWatched('${movie.id}')">Marcar como Assistido</button>
        `;
        list.appendChild(listItem);
    });
}

function markAsWatched(movieId) {
    fetch(`/markWatched?id=${movieId}`, { method: 'POST' })
        .then(() => alert("Filme marcado como assistido!"))
        .catch(err => console.error('Erro ao marcar filme como assistido', err));
}
