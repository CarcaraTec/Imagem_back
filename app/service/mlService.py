import pickle
import nltk
from nltk.corpus import stopwords
from deep_translator import GoogleTranslator

# carregar o modelo treinado
with open('app/files/lightgbm_model.pkl', 'rb') as f:
    lgbm_model = pickle.load(f)

# carregar o CountVectorizer
with open('app/files/tfidf_vectorizer_lgb.pkl', 'rb') as f:
    tfidf_vect = pickle.load(f)

def translate_to_english(text):
    translator = GoogleTranslator(source='auto', target='en')
    return translator.translate(text)

# definir stopwords como ingles
stop_words = set(stopwords.words('english'))

# prever o sentimento da frase
def predict_sentiment(text):
    translated_text = translate_to_english(text)
    print(translated_text)
    preprocessed_text = remove_stopwords(translated_text)
    text_vector = tfidf_vect.transform([preprocessed_text])
    sentiment = lgbm_model.predict(text_vector)[0]
    if sentiment == 2:
        return 'Positive'
    elif sentiment == 1:
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
    predicted_sentiment = predict_sentiment(input_text)
    sentiment = {
        'sentiment': predicted_sentiment
    }
    return sentiment