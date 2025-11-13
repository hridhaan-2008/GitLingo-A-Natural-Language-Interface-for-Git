#### `backend/app.py`
This is the core of your NLP engine and web server.

```python
import json
from flask import Flask, request, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask_cors import CORS

# Initialize Flask App and enable CORS
app = Flask(__name__)
CORS(app)

# --- NLP Engine Setup ---

# Load the corpus of Git commands and their intents
with open('corpus.json', 'r') as f:
    corpus_data = json.load(f)

# We need a flat list of all intent phrases and a mapping back to their command objects
intent_phrases = []
intent_to_command = []
for item in corpus_data:
    for phrase in item['intent_phrases']:
        intent_phrases.append(phrase)
        intent_to_command.append(item)

# Create and fit the TF-IDF Vectorizer
# This turns our text phrases into numerical vectors
vectorizer = TfidfVectorizer()
intent_vectors = vectorizer.fit_transform(intent_phrases)

# --- API Endpoint ---

@app.route('/api/translate', methods=['POST'])
def translate_query():
    try:
        data = request.get_json()
        user_query = data.get('query')

        if not user_query:
            return jsonify({"error": "Query is missing"}), 400

        # 1. Transform the user's query using the SAME vectorizer
        query_vector = vectorizer.transform([user_query])

        # 2. Calculate cosine similarity between the query and all known intents
        similarities = cosine_similarity(query_vector, intent_vectors).flatten()

        # 3. Find the index of the most similar intent phrase
        best_match_index = similarities.argmax()
        
        # 4. Get the confidence score of the best match
        confidence = similarities[best_match_index]

        # We'll only return a result if we're reasonably confident
        if confidence < 0.2: # This threshold can be tuned
            return jsonify({
                "command": "No confident match found.",
                "description": "Sorry, I couldn't understand that. Please try rephrasing."
            })

        # 5. Retrieve the corresponding command object using our map
        result = intent_to_command[best_match_index]
        
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
