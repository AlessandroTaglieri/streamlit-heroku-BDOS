import streamlit as st
from PIL import Image
import pandas as pd
image = Image.open('assets/sf_image.jpg')
dataset_path ='dataset/Restaurant_Scores_-_LIVES_Standard.csv'

def app():
    st.title('Dashboard - SF Restaurant Scores')
    st.image(image, use_column_width=True)
    st.header('Project goal')
    st.subheader('Restaurant inspections are very important for the prevention of food borne diseases. To predict if any restaurant is continually behaving in common pattern or is a periodic defaulter, machine learning can be used. This will in turn help in predicting future risk category for the restaurants and those with high risk category can be inspected on regular basis. In this paper we’ll understand the data recorded for each restaurant in San Francisco, California, recorded during inspection. This data will then be preprocessed and cleaned to remove any noise if present. Post cleaning the data it will be made to fit in different machine learning algorithms and models will be measured for their accuracy on predicting risk category. At the end various comparison between different models are done to select the best model for this dataset.')
    st.header('Dataset description')
    st.subheader('The Health Department has developed an inspection report and scoring system. After conducting an inspection of the facility, the Health Inspector calculates a score based on the violations observed. Violations can fall into:high risk category: records specific violations that directly relate to the transmission of food borne illnesses, the adulteration of food products and the contamination of food-contact surfaces.moderate risk category: records specific violations that are of a moderate risk to the public health and safety.low risk category: records violations that are low risk or have no immediate risk to the public health and safety.The score card that will be issued by the inspector is maintained at the food establishment and is available to the public in this dataset.')
    st.subheader('This dataset is available on the following link: https://data.sfgov.org/Health-and-Social-Services/Restaurant-Scores-LIVES-Standard/pyih-qa8i?row_index=0')
    st.header('Data overview')
    restaurant_dataset = pd.read_csv(dataset_path)
    st.dataframe(restaurant_dataset.head(20))
    