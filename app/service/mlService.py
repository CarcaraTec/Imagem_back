import pickle
import nltk
from nltk.corpus import stopwords
from deep_translator import GoogleTranslator
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Carregar o modelo treinado
with open('app/files/lightgbm_model.pkl', 'rb') as f:
    lgbm_model = pickle.load(f)

# Carregar o Vectorizer
with open('app/files/tfidf_vectorizer_lgb.pkl', 'rb') as f:
    tfidf_vect = pickle.load(f)

# modelo BERT para detecção de sarcasmo
tokenizer = AutoTokenizer.from_pretrained('nikesh66/Sarcasm-Detection-using-BERT')
sarcasm_model = AutoModelForSequenceClassification.from_pretrained('nikesh66/Sarcasm-Detection-using-BERT')

def translate_to_english(text):
    translator = GoogleTranslator(source='auto', target='en')
    return translator.translate(text)

stop_words = set(stopwords.words('english'))

def remove_stopwords(text):
    if isinstance(text, str):
        words = text.split()
        filtered_words = [word for word in words if word.lower() not in stop_words]
        return ' '.join(filtered_words)
    else:
        return ''

# Função para detectar sarcasmo
def detect_sarcasm(text):
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=512)
    outputs = sarcasm_model(**inputs)
    logits = outputs.logits
    probabilities = torch.softmax(logits, dim=-1).tolist()[0]
    sarcasm_probability = probabilities[1]  # Assuming the second index is the sarcasm class
    return sarcasm_probability

# Prever o sentimento da frase
def predict_sentiment(text):
    translated_text = translate_to_english(text)
    preprocessed_text = remove_stopwords(translated_text)
    text_vector = tfidf_vect.transform([preprocessed_text])
    sentiment = lgbm_model.predict(text_vector)[0]
    if sentiment == 2:
        return 'Positive'
    elif sentiment == 1:
        return 'Neutral'
    else:
        return 'Negative'

# Uso 
def predict_text(input_text):
    translated_text = translate_to_english(input_text)
    sarcasm_probability = detect_sarcasm(translated_text)
    if sarcasm_probability > 0.6:
        sentiment = {
            'sentiment': f'Sarcastic ({sarcasm_probability * 100:.2f}%)'
        }
    else:
        predicted_sentiment = predict_sentiment(input_text)
        sentiment = {
            'sentiment': predicted_sentiment
        }
    return sentiment
