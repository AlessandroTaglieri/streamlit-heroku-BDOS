import streamlit as st
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from PIL import Image
image = Image.open('assets/insp-2.jpg')
orange = Image.open('assets/orange.jpg')
green = Image.open('assets/green.jpg')
red = Image.open('assets/red.jpg')
def app():
    st.title('Insert your insepection text and make predictions')
    
    st.header('Do tou want to know risk category of inspected restaruant?')
    
    text = st.text_area('Insert here your violation description to know the predcited risk category (short text, suggested max 50 chars):', max_chars=50)
    
    st.write('You have inserted the following text: ', text)
    if text != '':
        with open('source/dict', "rb") as f:
            vocabulary_to_load = pickle.load(f)
            loaded_vectorizer = CountVectorizer(vocabulary=vocabulary_to_load)
            loaded_vectorizer._validate_vocabulary()
            

            with open('source/risk_prediction.pkl', 'rb') as file:
                model = pickle.load(file)

                prediction = model.predict(loaded_vectorizer.transform([text]))  
                if prediction == 1.0:
                    output='Low Risk' 
                elif prediction == 2.0:
                    output='Moderate Risk' 
                else:
                    output='High Risk' 
                st.write('Predicted RISK CATEGORY: ',output)
                if prediction == 1.0:
                    st.image(green, use_column_width=True)
                elif prediction == 2.0:
                    st.image(orange, use_column_width=True,width=70) 
                else:
                    st.image(red, use_column_width=True)
    else:
        st.image(image, use_column_width=True)
    