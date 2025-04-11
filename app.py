import streamlit as st
import numpy as np
import pickle
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
import string

# Load the trained model
with open('model_NB.pkl', 'rb') as file:
    model_NB = pickle.load(file)

# Load the vectorizer
with open('vectorizer.pkl', 'rb') as file:
    vectorizer = pickle.load(file)

st.title("Resume Classification")

inputs = []
feature_names = ["Mention skills relevant to your profession"]

for i in feature_names:
    value = st.text_input(i)
    inputs.append(value)

# Initialize stopwords and lemmatizer
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')


stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

# Function for text preprocessing
def preprocess_data(input_texts):
    preprocessed_texts = []
    for Resume in input_texts:
        lowered = Resume.lower()
        translator = str.maketrans('', '', string.punctuation)
        cleaned_text = lowered.translate(translator)
        tokenized = nltk.word_tokenize(cleaned_text)
        stop_words_removed = [word for word in tokenized if word not in stop_words]
        lemmatized = [lemmatizer.lemmatize(word) for word in stop_words_removed]
        preprocessed_texts.append(' '.join(lemmatized))
    return preprocessed_texts

# Preprocess input data
preprocessed_inputs = preprocess_data(inputs)

# Vectorize input data
user_input_vec = vectorizer.transform(preprocessed_inputs)

# Predict and display the result
if st.button("Discover My Career Fit"):
    prediction = model_NB.predict(user_input_vec)
    st.success(f'Model Prediction: {prediction[0]}')
