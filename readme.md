# 🎬 Movie Recommendation System

A content-based movie recommendation engine that suggests similar movies based on metadata like genres, keywords, cast, crew, and overview. Built with **Python**, **Scikit-learn**, and **Streamlit**.

> **Live Demo** — [Hugging Face Space](https://huggingface.co/spaces/ashish3120/Movie-Recomendation)

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
| Web UI         | Streamlit                                            |
| Vectorization  | `CountVectorizer` (Bag of Words)                     |
| Similarity     | Cosine Similarity (`sklearn.metrics.pairwise`)       |
| Deployment     | Hugging Face Spaces                                  |
| Model Hosting  | Hugging Face Datasets (for .pkl files > 200MB)       |

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
│   ├── movie_list.pkl          # Serialized DataFrame (hosted on HF Datasets)
│   └── similarity.pkl          # Precomputed similarity matrix (~200 MB, hosted on HF Datasets)
│
├── notebook/
│   └── recommender.ipynb       # Jupyter notebook — full ML pipeline (EDA → Model)
│
├── .gitattributes              # Git LFS tracking for .pkl files
├── .gitignore                  # Git ignore rules
├── requirements.txt            # Python dependencies
└── readme.md                   # Project documentation (this file)
```

---

## 🚀 Deployment

The application is deployed on **Hugging Face Spaces** using **Streamlit**. 

Due to the size of the precomputed similarity matrix (~200 MB), the `.pkl` files are hosted on **Hugging Face Datasets** and are dynamically downloaded when the application starts.

- **Space**: [ashish3120/Movie-Recomendation](https://huggingface.co/spaces/ashish3120/Movie-Recomendation)
- **Dataset**: [ashish3120/movies](https://huggingface.co/datasets/ashish3120/movies)

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
- [Hugging Face](https://huggingface.co/) — For hosting the app and datasets

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/ashish3120">Ashish</a>
</p>
