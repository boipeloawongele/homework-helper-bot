# Homework Helper: OCR + GPT-4 Answer Generator

import openai
import pytesseract
from PIL import Image
import streamlit as st
from googletrans import Translator

# Set your OpenAI API Key
openai.api_key = "YOUR_OPENAI_API_KEY"

def extract_text_from_image(image):
    text = pytesseract.image_to_string(image)
    return text

def get_gpt_answer(question, language="en"):
    system_msg = "You are a friendly homework assistant who explains things simply."
    if language != "en":
        question = Translator().translate(question, dest='en').text

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": question}
        ]
    )
    answer = response.choices[0].message.content

    if language != "en":
        answer = Translator().translate(answer, dest=language).text

    return answer

# Streamlit Interface
st.title("📚 Homework Helper for Busy Parents")
st.write("Snap or type a question and get a simple explanation")

option = st.radio("Choose input method:", ["Upload Photo", "Type Question"])

lang = st.selectbox("Choose Language", ["English", "Swahili", "Zulu", "French"])
lang_code = {"English": "en", "Swahili": "sw", "Zulu": "zu", "French": "fr"}[lang]

if option == "Upload Photo":
    uploaded_file = st.file_uploader("Upload an image of the question", type=["jpg", "png"])
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, caption="Uploaded Homework", use_column_width=True)
        question = extract_text_from_image(img)
        st.write("Extracted Question:", question)
        if st.button("Get Answer"):
            answer = get_gpt_answer(question, language=lang_code)
            st.success(answer)
else:
    question = st.text_area("Type your question here")
    if st.button("Get Answer") and question.strip():
        answer = get_gpt_answer(question, language=lang_code)
        st.success(answer)
