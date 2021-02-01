import streamlit as st
import pickle
from sklearn.feature_extraction.text import CountVectorizer
def app():

    text = st.text_area('Insert here your violation descriptio to know the predcited risk category')
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
    