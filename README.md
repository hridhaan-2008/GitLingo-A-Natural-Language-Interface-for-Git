# GitLingo: A Natural Language Interface for Git

GitLingo is a full-stack web application that translates plain English queries into their most likely Git command counterparts. This project aims to lower the barrier to entry for Git by allowing developers to describe their intent rather than having to recall specific syntax.

## Why it's Unique

Instead of simple keyword matching, GitLingo uses a Natural Language Processing (NLP) model to understand the *semantic meaning* of a user's query. This provides more accurate and intuitive results.

## How It Works

The application consists of a React frontend and a Python (Flask) backend that handles the AI logic.

1.  **Corpus:** The backend is powered by a `corpus.json` file, which contains a list of Git commands and multiple "intent phrases" for each.
2.  **Vectorization:** At startup, the server uses **scikit-learn's `TfidfVectorizer`** to convert all intent phrases into a matrix of numerical vectors. This vector represents the semantic essence of each phrase.
3.  **API Call:** The React frontend sends the user's query to a `/api/translate` endpoint on the Flask server.
4.  **Similarity Search:** The backend converts the user's query into a vector using the *same* vectorizer. It then calculates the **Cosine Similarity** between the user's vector and every vector in the intent matrix.
5.  **Result:** The command corresponding to the highest similarity score is returned to the frontend and displayed.

## Technology Stack

*   **Frontend:** React.js
*   **Backend:** Python with Flask
*   **NLP:** scikit-learn

## How to Run

### Backend
```bash
cd backend
pip install -r requirements.txt
python app.py
# Server will be running on http://127.0.0.1:5000
