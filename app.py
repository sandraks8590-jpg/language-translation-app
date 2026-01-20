import streamlit as st
import langdetect
from googletrans import Translator, LANGUAGES
import pickle

from langdetect import lang_detect_exception
lst=['English','Malayalam','Arabic','Tamil','Kannada','Hindi']
modelpath='pages/language.sav'
vectorpath='pages/vectorizer.sav'
with open(modelpath, 'rb') as f:
    model = pickle.load(f)

with open(vectorpath, 'rb') as f:
    vectorizer = pickle.load(f)


st.title("Language Detection and Translation")


text = st.text_area("Enter text:", height=100, key="language_input")



def detect_language_ml(text):
    text_tfidf = vectorizer.transform([text])
    prediction = model.predict(text_tfidf)
    return prediction[0]



def detect_language_langdetect(text):
    try:
        language = langdetect.detect(text)
    except lang_detect_exception.LangDetectException:
        language = 'unknown'
    return language




if st.button("Detect Language", key="detect_language_button"):
    detected_lang_ml = detect_language_ml(text)
    if detected_lang_ml == 0:
        l = "Arabic"
    elif detected_lang_ml == 1:
        l = "English"
    elif detected_lang_ml == 2:
        l = "Hindi"
    elif detected_lang_ml == 3:
        l = "Kannada"
    elif detected_lang_ml == 4:
        l = "Malayalam"
    elif detected_lang_ml == 5:
        l = "Tamil"
    else:
        l = "INVALID"
    detected_lang_langdetect = detect_language_langdetect(text)
    if detected_lang_langdetect == "ar":
        lg = "Arabic"
    elif detected_lang_langdetect == "en":
        lg = "English"
    elif detected_lang_langdetect == "hi":
        lg = "Hindi"
    elif detected_lang_langdetect == "kn":
        lg = "Kannada"
    elif detected_lang_langdetect == "ml":
        lg = "Malayalam"
    elif detected_lang_langdetect == "ta":
        lg = "Tamil"
    else:
        lg = "Invalid"
    st.write(f"Detected Language (ML Model): {l}")
    st.write(f"Detected Language (langdetect): {lg}")

translator = Translator()
supported_languages = ["en", "ar", "hi", "ml", "ta"]
language_names = {
    "en": "English",
    "ar": "Arabic",
    "hi": "Hindi",
    "ml": "Malayalam",
    "ta": "Tamil"
}
language_options = [language_names[lang] for lang in supported_languages]


source_lang = st.selectbox("Select source language:", language_options)
target_lang = st.selectbox("Select target language:", language_options)

source_lang_code = [k for k, v in language_names.items() if v == source_lang][0]
target_lang_code = [k for k, v in language_names.items() if v == target_lang][0]




if st.button("Translate"):
    try:
        result = translator.translate(text, src=source_lang_code, dest=target_lang_code)
        st.write(f"Translated Text ({language_names[target_lang_code]}): {result.text}")
    except Exception as e:
        st.error(f"Error: {str(e)}")