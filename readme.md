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

## 🚀 Getting Started

### Prerequisites

- Python **3.14** or higher
- pip (Python package manager)
- Git LFS (for pulling large `.pkl` model files)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/ashish3120/Movie-Recomendation-System.git
cd Movie-Recomendation-System

# 2. (Required) Pull Git LFS files
git lfs install
git lfs pull

# 3. Create a virtual environment (recommended)
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Download NLTK data (one-time)
python -c "import nltk; nltk.download('punkt')"
```

### Run the App

```bash
cd app
streamlit run app.py
```

The app will open at **http://localhost:8501** in your browser.

### Re-train the Model (Optional)

If you want to re-train or modify the model:

```bash
cd notebook
jupyter notebook recommender.ipynb
```

Run all cells — this will regenerate `model/movie_list.pkl` and `model/similarity.pkl`.

---

## 🌐 Deploying on Render

> See the detailed deployment guide below.

### Step 1 — Push All Files to GitHub

Make sure your repository includes:
- `requirements.txt` (created in this repo)
- `render.yaml` (created in this repo)
- Model files tracked via **Git LFS**

```bash
git add .
git commit -m "Add deployment files"
git push origin main
```

### Step 2 — Create a Render Web Service

1. Go to [https://render.com](https://render.com) and sign in with GitHub.
2. Click **"New +"** → **"Web Service"**.
3. Connect your **Movie-Recomendation-System** GitHub repository.
4. Configure the service:

| Setting         | Value                                              |
| --------------- | -------------------------------------------------- |
| **Name**        | `movie-recommender-api`                             |
| **Runtime**     | `Python`                                           |
| **Build Command** | `pip install -r requirements.txt`                |
| **Start Command** | `uvicorn app.api:app --host 0.0.0.0 --port $PORT` |
| **Plan**        | Free                                               |

5. Click **"Create Web Service"**.

### Step 3 — Enable Git LFS on Render

Since `similarity.pkl` is tracked by Git LFS (~208 MB), Render needs to pull LFS files during the build. Add this **environment variable** in your Render dashboard:

| Key                  | Value  |
| -------------------- | ------ |
| `GIT_LFS_ENABLED`   | `true` |

> ⚠️ **Important**: Render's free tier has limited disk and memory. The similarity matrix is ~208 MB. If you hit memory limits, consider upgrading to the **Starter plan ($7/month)** which provides 512 MB RAM and 1 GB disk.

### Step 4 — Fix the Model Path for Deployment

The current `app.py` uses relative paths (`../model/...`). For Render, the working directory might differ. The `render.yaml` included in this repo handles this via the `cd app &&` prefix in the start command which ensures the correct relative path resolution.

### Step 5 — Verify

Once deployed, Render will provide a URL like:
```
https://movie-recommender-xxxx.onrender.com
```

Visit the URL to verify your app is live!

---

## ⚙️ Render Configuration (render.yaml)

The `render.yaml` file auto-configures everything when you connect the repo to Render:

```yaml
services:
  # 1. Backend API (FastAPI)
  - type: web
    name: movie-recommender-api
    runtime: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app.api:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: GIT_LFS_ENABLED
        value: true
      - key: PYTHON_VERSION
        value: 3.14.3
  
  # 2. Frontend (Static Site)
  - type: static
    name: movie-recommender-frontend
    publishDir: frontend
    buildCommand: ""
```

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
