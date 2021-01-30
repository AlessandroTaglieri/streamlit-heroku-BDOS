
def app():
    import streamlit as st

    import pandas as pd
    import numpy as np
    import folium
    import datetime
    import streamlit as st
    from streamlit_folium import folium_static
    import folium
    dataset_path ='dataset/Restaurant_Scores_-_LIVES_Standard.csv'
    restaurant_dataset = pd.read_csv(dataset_path)
    restaurant_dataset.info()
    restaurant_dataset['violation_id'] = restaurant_dataset.violation_id.str.split('_').str[2]
    #replacing typos to null values as postal code is not known
    replace_ca_value = dict.fromkeys(['CA', 'Ca', '941'], np.nan)
    restaurant_dataset = restaurant_dataset.replace(replace_ca_value)
    #making postal code in symmetry with 5 digits only
    restaurant_dataset.business_postal_code = restaurant_dataset.business_postal_code.str[:5]

    restaurant_dataset=restaurant_dataset.dropna(subset=['Supervisor Districts','business_postal_code','inspection_score'])
    restaurant_dataset = restaurant_dataset.dropna(axis=0, subset=['business_longitude', 'violation_description'])
    restaurant_dataset=restaurant_dataset.dropna(subset=['risk_category'])
    #take only date and not time
    #restaurant_dataset['inspection_date'] = restaurant_dataset['inspection_date'].str[:10]
    restaurant_dataset['inspection_date_p'] = pd.to_datetime(restaurant_dataset['inspection_date'])

    st.title('Top & Flop Restaurants')

    st.header('Flop five restaurants')
    st.subheader('Table: Risk category distribution over top 5 restaurants')
    today = datetime.date.today()
    restaurant_dataset['inspection_date_p'] = restaurant_dataset['inspection_date_p'].astype('str')
    restaurant_dataset['inspection_date_p'] = pd.to_datetime(restaurant_dataset['inspection_date_p'])
    data = restaurant_dataset.set_index('inspection_date_p')
    
    worst_yr = restaurant_dataset.groupby(['business_name','risk_category'])['violation_id'].count()
    worst_yr = pd.DataFrame(worst_yr)
    worst_yr.reset_index(inplace=True)
    worst_yr = worst_yr.pivot(index='business_name',columns='risk_category',values='violation_id').fillna(value=0)
    worst_yr.columns = ['High Risk', 'Low Risk', 'Moderate Risk']
    worst_yr.head()
    worst_yr = worst_yr.sort_values(['High Risk', 'Moderate Risk', 'Low Risk'], ascending=False)
    worst_yr['total'] = worst_yr['High Risk']+worst_yr['Low Risk']+worst_yr['Moderate Risk']
    worst_yr = worst_yr.loc[worst_yr['total']>20].head()
    del worst_yr['total']
    st.dataframe(worst_yr, width=700)
    
    st.subheader('Pie chart: Risk category distribution over top 5 restaurants')
    st.bar_chart(worst_yr, width=700,height=500)

    st.header('Top five restaurants')
    best_yr = restaurant_dataset.groupby(['business_name','risk_category'])['violation_id'].count()
    best_yr = pd.DataFrame(best_yr)
    best_yr.reset_index(inplace=True)
    best_yr = best_yr.pivot(index='business_name',columns='risk_category',values='violation_id').fillna(value=0)
    best_yr.columns = ['High Risk', 'Low Risk', 'Moderate Risk']
    best_yr.head()
    best_yr = best_yr.sort_values(['High Risk', 'Moderate Risk', 'Low Risk'], ascending=True)
    best_yr['total'] = best_yr['High Risk']+best_yr['Low Risk']+best_yr['Moderate Risk']
    best_yr = best_yr.loc[best_yr['total']>20].head()
    del best_yr['total']
    st.dataframe(best_yr, width=700)
    #worst_yr=worst_yr.transpose()
    #st.dataframe(worst_yr)
    st.subheader('Pie chart: Risk category distribution over top 5 restaurants')
    st.bar_chart(best_yr, width=700,height=500)
 