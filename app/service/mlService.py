import pickle
import nltk
from nltk.corpus import stopwords

# carregar o modelo treinado
with open('app/files/logistic_regression_model.pkl', 'rb') as f:
    clf = pickle.load(f)

# carregar o CountVectorizer
with open('app/files/count_vectorizer.pkl', 'rb') as f:
    vect = pickle.load(f)

# definir stopwords como ingles
stop_words = set(stopwords.words('english'))

# pré-processar a frase de entrada
def preprocess_text(text):
    text_vect = vect.transform([text])
    return text_vect

# prever o sentimento da frase
def predict_sentiment(text):
    text_vect = preprocess_text(text)
    sentiment = clf.predict(text_vect)
    if sentiment == 1:
        return 'Positive'
    elif sentiment == 0:
        return 'Neutral'
    else:
        return 'Negative'
    
# função de remover stopwords do texto
def remove_stopwords(text):
    if isinstance(text, str):
        words = text.split()
        filtered_words = [word for word in words if word.lower() not in stop_words]
        return ' '.join(filtered_words)
    else:
        return ''
    
# uso
def predict_text(input_text):
    text = remove_stopwords(input_text)
    predicted_sentiment = predict_sentiment(text)
    sentiment = {
        'sentiment': predicted_sentiment
    }
    return sentiment