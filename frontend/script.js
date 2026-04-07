// REPLACE THIS WITH YOUR RENDER API URL ONCE DEPLOYED
const API_BASE_URL = "https://movie-recomendation-system-api.onrender.com"; // Default placeholder

let allMovies = [];

document.addEventListener("DOMContentLoaded", () => {
    fetchMovies();
    setupSearch();
    
    document.getElementById("recommend-btn").addEventListener("click", getRecommendations);
});

// Fetch movie list for autocomplete
async function fetchMovies() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/movies`);
        if (!response.ok) throw new Error("Failed to fetch movies");
        
        const data = await response.json();
        allMovies = data.movies;
        
        document.getElementById("movie-count").textContent = `${allMovies.length} Movies Analyzed`;
    } catch (error) {
        console.error("Error loading movies:", error);
        document.getElementById("movie-count").textContent = "API Offline";
    }
}

// Setup search autocomplete logic
function setupSearch() {
    const searchInput = document.getElementById("movie-search");
    const dropdown = document.getElementById("search-dropdown");
    const btn = document.getElementById("recommend-btn");

    searchInput.addEventListener("input", (e) => {
        const val = e.target.value.toLowerCase();
        dropdown.innerHTML = "";
        
        if (!val) {
            dropdown.style.display = "none";
            btn.disabled = true;
            return;
        }

        const filtered = allMovies
            .filter(m => m.toLowerCase().includes(val))
            .slice(0, 8);

        if (filtered.length > 0) {
            filtered.forEach(m => {
                const item = document.createElement("div");
                item.className = "dropdown-item";
                item.textContent = m;
                item.addEventListener("click", () => {
                    searchInput.value = m;
                    dropdown.style.display = "none";
                    btn.disabled = false;
                });
                dropdown.appendChild(item);
            });
            dropdown.style.display = "block";
        } else {
            dropdown.style.display = "none";
        }
        
        // Exact match check
        btn.disabled = !allMovies.includes(searchInput.value);
    });

    // Close dropdown on click outside
    document.addEventListener("click", (e) => {
        if (!document.getElementById("search-wrapper").contains(e.target)) {
            dropdown.style.display = "none";
        }
    });

    // Allow Enter key to trigger recommendation
    searchInput.addEventListener("keypress", (e) => {
        if (e.key === "Enter" && !btn.disabled) {
            getRecommendations();
        }
    });
}

// Fetch recommendations from API
async function getRecommendations() {
    const movie = document.getElementById("movie-search").value;
    const btn = document.getElementById("recommend-btn");
    const btnText = btn.querySelector(".btn-text");
    const loader = document.getElementById("btn-loader");
    const arrow = btn.querySelector(".btn-arrow");
    const resultsSection = document.getElementById("results-section");

    // Loading state
    btn.disabled = true;
    btnText.textContent = "Analyzing Similarity...";
    loader.style.display = "block";
    arrow.style.display = "none";

    try {
        const response = await fetch(`${API_BASE_URL}/api/recommend`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ movie })
        });

        if (!response.ok) throw new Error("Recommendation failed");

        const data = await response.json();
        
        // Update UI
        document.getElementById("queried-movie").textContent = movie;
        renderRecommendations(data.recommendations);
        
        resultsSection.style.display = "block";
        resultsSection.scrollIntoView({ behavior: "smooth", block: "start" });

    } catch (error) {
        console.error("Error:", error);
        alert("An error occurred while fetching recommendations. Please try again.");
    } finally {
        // Reset state
        btn.disabled = false;
        btnText.textContent = "Get Recommendations";
        loader.style.display = "none";
        arrow.style.display = "block";
    }
}

// Render the results grid
function renderRecommendations(movies) {
    const grid = document.getElementById("results-grid");
    grid.innerHTML = "";

    const icons = ["🎬", "🍿", "🎥", "🎞️", "📽️"];

    movies.forEach((title, index) => {
        const card = document.createElement("div");
        card.className = "movie-card";
        
        card.innerHTML = `
            <div class="movie-poster-placeholder">${icons[index % icons.length]}</div>
            <div class="movie-info">
                <h3 class="movie-title">${title}</h3>
            </div>
        `;
        
        grid.appendChild(card);
    });
}
