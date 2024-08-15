document.addEventListener('DOMContentLoaded', () => {
    fetchMovies();
});

function fetchMovies() {
    fetch('http://127.0.0.1/movies')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(movies => {
            displayMovieDates(movies);
            populateDateSelect(movies);
        })
        .catch(error => console.error('Error fetching movies:', error));
}

function displayMovieDates(movies) {
    const container = document.getElementById('movie-dates-container');
    container.innerHTML = movies.map((movie, index) => generateMovieDateHTML(movie, index)).join('');
}

function populateDateSelect(movies) {
    const dateSelect = document.getElementById('date');
    movies.forEach(movie => {
        const option = document.createElement('option');
        option.value = movie.id; // Assuming you want to use the movie ID as the value
        option.textContent = `${movie.title} - ${movie.description}`;
        dateSelect.appendChild(option);
    });
}

function generateMovieDateHTML(movie, index) {
    return `
        <div class="card">
            <div class="card-header" id="heading${index}">
                <h2 class="mb-0">
                    <button class="btn btn-link text-decoration-none text-dark" type="button" data-bs-toggle="collapse" data-bs-target="#collapse${index}" aria-expanded="true" aria-controls="collapse${index}">
                        <img src="../assets/front.jpg" alt="${movie.title}" width="100" height="100">
                        ${movie.title}
                    </button>
                </h2>
            </div>
            <div id="collapse${index}" class="collapse" aria-labelledby="heading${index}" data-bs-parent="#movie-dates-container">
                <div class="card-body">
                    <p><strong>Description:</strong> ${movie.description}</p>
                </div>
            </div>
        </div>
    `;
}   