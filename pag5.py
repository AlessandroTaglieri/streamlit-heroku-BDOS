import streamlit as st
def app():

    text = st.text_area('Insert here your violation descriptio to know the predcited risk category')
    st.write('You have inserted the following text: ', text)

    