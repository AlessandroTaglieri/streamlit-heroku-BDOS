
def app():
    import streamlit as st
    import datetime
    import pandas as pd
    import numpy as np
    import folium
    from  matplotlib import pyplot as plt
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
    

    st.title('Maps over insepctions')
    restaurant_dataset['inspection_date_p'] = pd.to_datetime(restaurant_dataset['inspection_date'])
    restaurant_dataset['inspection_date_p'] = restaurant_dataset['inspection_date_p'].dt.to_period('M')
    data_low = restaurant_dataset.loc[restaurant_dataset['risk_category'] ==  'Low Risk']
    data_high = restaurant_dataset.loc[restaurant_dataset['risk_category'] ==  'High Risk']
    data_moderate = restaurant_dataset.loc[restaurant_dataset['risk_category'] ==  'Moderate Risk']
    data = restaurant_dataset.groupby('inspection_date_p')['inspection_id'].nunique()
    data = pd.DataFrame({'date':data.index, 'inspections':data.values})
    data['date'] = data['date'].astype('str')
    date = list(data.date)
    values = list(data.inspections)
    data_low = data_low.groupby('inspection_date_p')['inspection_id'].nunique()
    data_low = pd.DataFrame({'date':data_low.index, 'inspections':data_low.values})
    data_high = data_high.groupby('inspection_date_p')['inspection_id'].nunique()
    data_high = pd.DataFrame({'date':data_high.index, 'inspections':data_high.values})
    data_moderate = data_moderate.groupby('inspection_date_p')['inspection_id'].nunique()
    data_moderate = pd.DataFrame({'date':data_moderate.index, 'inspections':data_moderate.values})
    data_low['date'] = data_low['date'].astype('str')
    date = list(data.date)
    values_low = list(data_low.inspections)
    values_high = list(data_high.inspections)
    values_moderate = list(data_moderate.inspections)
    
    dict2 = {'date': date, 'Low': values_low, 'High': values_high, 'Moderate': values_moderate}  
    df = pd.DataFrame(dict2)
    df = df.set_index('date')
    
    st.line_chart(df,width=700,height=400)
  
    st.header('aaa')
    restaurant_dataset['inspection_date_p'] = pd.to_datetime(restaurant_dataset['inspection_date'])
    # Score relation with date of the inspection, is there bias?
    date = restaurant_dataset.groupby('business_id')['inspection_date_p','inspection_score'].max()
    weekday = date.inspection_date_p.dt.weekday
    import chart_studio.plotly as po
    import plotly.graph_objs as go
    from plotly.offline import init_notebook_mode, iplot
    init_notebook_mode()
    # sepcify that we want a scatter plot with, with date on the x axis and meet on the y axis
    graph_data = [go.Scatter(x=date.inspection_date_p, 
                            y=date.inspection_score,
                            mode='markers',
                            marker=dict(
                                color=weekday,
                                colorscale='Viridis',
                                showscale=True,
                                colorbar=dict(
                                    title='Weekday'
                                )
                            )
                            )
                ]

    # specify the layout of our figure
    layout = dict(title = "Score vs Time",
                xaxis= dict(title= 'Date',ticklen= 5,zeroline= False),
                yaxis=dict(title="Inspection Score"),
                width=1000,
       
                )

    # create and show our figure
    fig = dict(data = graph_data, 
            layout = layout)
    st.plotly_chart(fig)

    
    st.header('Distribution over the risk category')
    low_risk = restaurant_dataset.loc[restaurant_dataset['risk_category']=='Low Risk'] 
    moderate_risk = restaurant_dataset.loc[restaurant_dataset['risk_category']=='Moderate Risk'] 
    high_risk = restaurant_dataset.loc[restaurant_dataset['risk_category']=='High Risk'] 
    
    data = {'Quantity': [len(high_risk), len(moderate_risk), len(low_risk)], 'Type':['High Risk','Moderate Risk','Low Risk']}
    
    df = pd.DataFrame.from_dict(data)
    df = df.set_index('Type')
    
    st.bar_chart(df, width=600,height=500)


    st.header('Distribution over the risk category')

    #converting violation type to 4 categories 'Hygiene','Legal','Noncompliance', 'Lack_Infrastructure'
    violation_hygiene = dict.fromkeys(['Unclean or degraded floors walls or ceilings', 'Wiping cloths not clean or properly stored or inadequate sanitizer', 'Moderate risk vermin infestation', 'Unclean nonfood contact surfaces', 'Foods not protected from contamination', 'Unclean hands or improper use of gloves', 'High risk vermin infestation', 'Inadequately cleaned or sanitized food contact surfaces', 'Low risk vermin infestation', 'Unclean or unsanitary food contact surfaces', 'Employee eating or smoking', 'Contaminated or adulterated food', 'Unsanitary employee garments hair or nails', 'Other low risk violation', 'Unclean unmaintained or improperly constructed toilet facilities', 'Other moderate risk violation', 'Sewage or wastewater contamination', 'Food in poor condition', 'Other high risk violation', 'Reservice of previously served foods', 'Discharge from employee nose mouth or eye', 'Improperly washed fruits and vegetables'], 'Hygiene')
    violation_lack_infra = dict.fromkeys(['No restroom facility within 200 feet of mobile food facility','Inadequate and inaccessible handwashing facilities', 'Inadequate or unsanitary refuse containers or area or no garbage service', 'No thermometers or uncalibrated thermometers', 'Improper or defective plumbing', 'No hot water or running water', 'Inadequate ventilation or lighting', 'Inadequate warewashing facilities or equipment', 'Inadequate sewage or wastewater disposal', 'Insufficient hot water or running water'],'Lack_Infrastructure')
    violation_legal = dict.fromkeys(['Food safety certificate or food handler card not available', 'Unapproved or unmaintained equipment or utensils', 'Permit license or inspection report not posted', 'No plan review or Building Permit', 'Unapproved  living quarters in food facility', 'Unpermitted food facility', 'Unapproved food source', 'Mobile food facility stored in unapproved location', 'Mobile food facility not operating with an approved commissary'],'Legal')
    violation_noncompliance = dict.fromkeys(['Improperly displayed mobile food permit or signage','Mobile food facility with unapproved operating conditions','High risk food holding temperature', 'Inadequate food safety knowledge or lack of certified food safety manager', 'Improper storage of equipment utensils or linens', 'Improper food storage', 'Improper thawing methods', 'Moderate risk food holding temperature', 'Improper cooling methods', 'Improper storage use or identification of toxic substances', 'Improper food labeling or menu misrepresentation', 'Non service animal', 'Noncompliance with shell fish tags or display', 'Noncompliance with HAACP plan or variance', 'Inadequate HACCP plan record keeping', 'Inadequate dressing rooms or improper storage of personal items', 'Improper reheating of food', 'Inadequate procedures or records for time as a public health control', 'Worker safety hazards', 'No person in charge of food facility', 'Improper cooking time or temperatures', 'Unauthorized or unsafe use of time as a public health control measure', 'Consumer advisory not provided for raw or undercooked foods', 'Noncompliance with Gulf Coast oyster regulation', 'Noncompliance with Cottage Food Operation'],'Noncompliance')


    restaurant_dataset = restaurant_dataset.replace(violation_hygiene)
    restaurant_dataset = restaurant_dataset.replace(violation_lack_infra)
    restaurant_dataset = restaurant_dataset.replace(violation_legal)
    restaurant_dataset = restaurant_dataset.replace(violation_noncompliance)
    a = restaurant_dataset['violation_description'].value_counts()
    data = pd.DataFrame({'violation_description':a.index, 'count':a.values})
    # only "explode" the 2nd slice (i.e. 'Hogs')
    explode = (0, 0.1, 0, 0)
    #add colors
    colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99']
    fig, ax = plt.subplots()
    ax.pie('count', labels = 'violation_description', data=data,colors=colors, autopct='%1.1f%%', explode=explode, )

    st.pyplot(fig)
   