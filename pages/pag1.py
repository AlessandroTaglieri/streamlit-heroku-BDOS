
def app():
    import streamlit as st

    import pandas as pd
    import numpy as np
    import folium

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

    st.title('Inspections over the map')
    st.subheader('This map representsrestaurant in San Francisco map. Every marker has a different colour based on their inspextion score')
    
   


    score_partial = restaurant_dataset.groupby('business_id')['business_latitude','business_longitude',
                                        'inspection_score'].mean()
    # Add names
    data = restaurant_dataset.set_index('inspection_date_p')
    names = data.business_name
    names.index = data.business_id

    score=score_partial.join(names.drop_duplicates(),how='left')
    import chart_studio.plotly as po
    import plotly.graph_objs as go
    from plotly.offline import init_notebook_mode, iplot
    from plotly.offline import init_notebook_mode, iplot
    init_notebook_mode()

    # Scatter plot in a map
    graph_data = [
        go.Scattermapbox(
            lat=score.business_latitude,
            lon=score.business_longitude,
            mode='markers',
            marker=dict(
                size=7,
                color=score.inspection_score,
                colorscale='Viridis',
                colorbar=dict(
                    title='Inspection Score'
                )
            ),
            text=score.business_name,
        )
    ]
    # specify the layout of our figure
    access_token='pk.eyJ1IjoibWFyaWFndW1iYW8iLCJhIjoiY2pwdmpwdGNyMGJzMTQzcWsyZjJjNHRzeiJ9.Xyr7tHeDm3VXHLMfYvPNHQ'
    layout = go.Layout(
        width=800,
        height=800,
        autosize=True,
        hovermode='closest',
        
        xaxis= dict(title= 'Date',ticklen= 5,zeroline= False),
        yaxis=dict(title="Inspection Score"),
        mapbox=dict(
            accesstoken=access_token,
            bearing=0,
            center=dict(
                lat=score.business_latitude.mean(),
                lon=score.business_longitude.mean()
            ),
            pitch=0,
            zoom=11,
            style='light'
        ),
    )

    # create and show our figure
    fig = dict(data = graph_data, 
            layout = layout)
    
    st.plotly_chart(fig)

    st.subheader('The following map represents a specific number of restaurants (default to 50). Every restaurant is represented by a marker that can be red, orange or green (by their risk category). If you can click on the marker, you can see the nameof the restaurant and its insepction description')
    number = st.number_input('Insert a number', 10,200)

    st.write('You have selected ', number, ' restaurants')
    SF_COORDINATES = (37.76, -122.45)
   
    import streamlit as st
    from streamlit_folium import folium_static
    import folium
    map = folium.Map(location=SF_COORDINATES, zoom_start=12) 

    # add a marker for every record in the filtered data, use a clustered view
    for each in restaurant_dataset[:int(number)].iterrows():
        if each[1]["risk_category"]=='High Risk':
            folium.Marker([each[1]["business_latitude"],
                        each[1]["business_longitude"]],
                        popup=each[1]["business_name"].replace("'", "") + ": " + each[1]["violation_description"],icon=folium.Icon(color='red')).add_to(map)
        elif each[1]["risk_category"]=='Low Risk' :
            folium.Marker([each[1]["business_latitude"],
                        each[1]["business_longitude"]],
                        popup=each[1]["business_name"].replace("'", "") + ": " + each[1]["violation_description"],icon=folium.Icon(color='green')).add_to(map)

        else:
            folium.Marker([each[1]["business_latitude"],
                        each[1]["business_longitude"]],
                        popup=each[1]["business_name"].replace("'", "") + ": " + each[1]["violation_description"],icon=folium.Icon(color='orange')).add_to(map)


    
        # call to render Folium map in Streamlit
    folium_static(map)