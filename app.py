import pickle
import nltk
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import string
from sklearn.feature_extraction.text import CountVectorizer
from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask(__name__)

# Download necessary NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

# Initialize the PorterStemmer and load stopwords
ps = PorterStemmer()
stop_words = set(stopwords.words('english'))

def convert_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)
    y = []
    for i in text:
        if i not in stop_words and i not in string.punctuation:
            stemmed = ps.stem(i)
            y.append(stemmed)
    return ' '.join(y)

# Load trained model and vectorizer
with open('model.pkl', 'rb') as model_file:
    mnb = pickle.load(model_file)

with open('vectorizer.pkl', 'rb') as vectorizer_file:
    cv = pickle.load(vectorizer_file)

def predict(text):
    try:
        text = convert_text(text)
        X = cv.transform([text])
        prediction = mnb.predict(X)[0]
        return 'Positive Review' if prediction == 1 else 'Negative Review'
    except Exception as e:
        return f"Error processing the text: {str(e)}"

@app.route('/predict', methods=['POST'])
def predict_route():
    data = request.json
    review_text = data.get('text', '')
    if not review_text:
        return jsonify({'error': 'No text provided'}), 400
    result = predict(review_text)
    return jsonify({'prediction': result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5667)
