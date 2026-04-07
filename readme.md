# 🎬 Movie Recommendation System

A content-based movie recommendation engine that suggests similar movies based on metadata like genres, keywords, cast, crew, and overview. Built with **Python**, **Scikit-learn**, and **Streamlit**.

> **Live Demo** — _Coming soon (deploying on Render)_

---

## 📸 Preview

<!-- Add a screenshot of the Streamlit app here -->
<!-- ![App Screenshot](assets/screenshot.png) -->

---

## 🧠 How It Works

```
┌─────────────┐    ┌──────────────────┐    ┌─────────────────┐    ┌──────────────┐
│  TMDB 5000  │───▶│  Feature Engg.   │───▶│  Count Vector.  │───▶│   Cosine     │
│  Dataset    │    │  (Tags Column)   │    │  (Bag of Words) │    │  Similarity  │
└─────────────┘    └──────────────────┘    └─────────────────┘    └──────┬───────┘
                                                                         │
                                                                         ▼
                                                                  ┌──────────────┐
                                                                  │  Top 5 Most  │
                                                                  │  Similar     │
                                                                  │  Movies      │
                                                                  └──────────────┘
```

### Algorithm Pipeline

1. **Data Merging** — Merge `tmdb_5000_movies.csv` and `tmdb_5000_credits.csv` on `title`.
2. **Feature Extraction** — Extract names from JSON-like columns (`genres`, `keywords`, `cast`, `crew`).
3. **Tag Creation** — Concatenate `overview + genres + keywords + top 3 cast + director` into a single `tags` column.
4. **Text Preprocessing** — Lowercase conversion, space removal in multi-word names, and **Porter Stemming** to normalize words (e.g., _loving → love_).
5. **Vectorization** — Convert tags to numerical vectors using `CountVectorizer` (Bag of Words, max 2000 features, English stop words removed).
6. **Similarity Computation** — Compute pairwise **Cosine Similarity** between all movie vectors.
7. **Recommendation** — For a given movie, sort all other movies by similarity score and return the **top 5**.

---

## 🛠️ Tech Stack

| Layer          | Technology                                           |
| -------------- | ---------------------------------------------------- |
| Language       | Python 3.14+                                         |
| ML / NLP       | Scikit-learn, NLTK (Porter Stemmer), Pandas, NumPy   |
| Backend API    | FastAPI, Uvicorn                                     |
| Web UI         | HTML5, CSS3 (Modern Vanilla), JavaScript (ES6+)      |
| Vectorization  | `CountVectorizer` (Bag of Words)                     |
| Similarity     | Cosine Similarity (`sklearn.metrics.pairwise`)       |
| Deployment     | Render (Web Service + Static Site)                   |

---

## 📁 Project Structure

```
Movie-Recomendation-System/
│
├── app/
│   └── app.py                  # Streamlit web application
│
├── dataset/
│   ├── tmdb_5000_movies.csv    # Movie metadata (genres, keywords, overview, etc.)
│   └── tmdb_5000_credits.csv   # Cast and crew data
│
├── model/
│   ├── movie_list.pkl          # Serialized DataFrame with movie_id, title, tags
│   └── similarity.pkl          # Precomputed cosine similarity matrix (~208 MB, Git LFS)
│
├── notebook/
│   └── recommender.ipynb       # Jupyter notebook — full ML pipeline (EDA → Model)
│
├── .gitattributes              # Git LFS tracking for .pkl files
├── .gitignore                  # Git ignore rules
├── requirements.txt            # Python dependencies
├── render.yaml                 # Render deployment configuration
└── readme.md                   # Project documentation (this file)
```

---

# 🚀 Deployment Guides

## 1. Backend (Render)
- Deploy your repo to Render as a **Web Service**.
- Set the **Start Command** to `uvicorn app.api:app --host 0.0.0.0 --port $PORT`.
- Set Environment Variable `GIT_LFS_ENABLED = true`.
- Set Environment Variable `PYTHON_VERSION = 3.14.3`.

## 2. Frontend (Vercel) — ✨ Recommended
Vercel is the fastest and easiest way to host your modern CSS/JS frontend.

1. Go to [https://vercel.com](https://vercel.com) and sign in with GitHub.
2. Click **"Add New"** → **"Project"**.
3. Import your `Movie-Recomendation-System` repository.
4. In **Project Settings**:
    - **Root Directory**: Select `frontend`.
    - **Build Settings**: Since it's vanilla HTML/CSS/JS, leave them at defaults.
5. Click **"Deploy"**.

Once deployed, copy your Vercel URL and add it to your portfolio!

---

## 📊 Dataset

The project uses the **TMDB 5000 Movie Dataset** from Kaggle:

- [`tmdb_5000_movies.csv`](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata) — 4,803 movies with budget, genres, keywords, overview, popularity, revenue, etc.
- [`tmdb_5000_credits.csv`](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata) — Cast and crew details for each movie.

---

## 🤝 Contributing

Contributions are welcome! Here's how:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🙏 Acknowledgements

- [TMDB 5000 Movie Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata) — Kaggle
- [Streamlit](https://streamlit.io/) — Web framework for ML apps
- [Scikit-learn](https://scikit-learn.org/) — ML library

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/ashish3120">Ashish</a>
</p>
