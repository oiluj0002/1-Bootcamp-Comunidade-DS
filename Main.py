#========================================================
# IMPORT LIBRARIES
#========================================================
import pandas as pd
import numpy as np
import folium
import plotly.express as px
import streamlit as st
from streamlit_folium import folium_static

#=======================================================
# FUNCTIONS
#=======================================================
def clean_data( df1 ):
    df1 = df1.dropna()

    return df1

def price_by_region( df1 ):
    df2 = df1.loc[:,['price','neighbourhood_group']].groupby('neighbourhood_group').mean().reset_index()
    fig = px.bar(df2, x='neighbourhood_group', y='price')

    return fig

def new_york_city_map( df1 ):

    linhas_select = df1['neighbourhood_group'] == 'Brooklyn'
    df_brooklyn = df1.loc[linhas_select, ['id','number_of_reviews', 'neighbourhood_group', 'latitude', 'longitude']].groupby(['neighbourhood_group','id', 'latitude', 'longitude']).max().sort_values('number_of_reviews', ascending=False).reset_index().head(10)

    linhas_select = df1['neighbourhood_group'] == 'Manhattan'
    df_manhattan = df1.loc[linhas_select, ['id','number_of_reviews', 'neighbourhood_group', 'latitude', 'longitude']].groupby(['neighbourhood_group','id', 'latitude', 'longitude']).max().sort_values('number_of_reviews', ascending=False).reset_index().head(10)

    linhas_select = df1['neighbourhood_group'] == 'Queens'
    df_queens = df1.loc[linhas_select, ['id','number_of_reviews', 'neighbourhood_group', 'latitude', 'longitude']].groupby(['neighbourhood_group','id', 'latitude', 'longitude']).max().sort_values('number_of_reviews', ascending=False).reset_index().head(10)

    linhas_select = df1['neighbourhood_group'] == 'Staten Island'
    df_staten = df1.loc[linhas_select, ['id','number_of_reviews', 'neighbourhood_group', 'latitude', 'longitude']].groupby(['neighbourhood_group','id', 'latitude', 'longitude']).max().sort_values('number_of_reviews', ascending=False).reset_index().head(10)

    linhas_select = df1['neighbourhood_group'] == 'Bronx'
    df_bronx = df1.loc[linhas_select, ['id','number_of_reviews', 'neighbourhood_group', 'latitude', 'longitude']].groupby(['neighbourhood_group','id', 'latitude', 'longitude']).max().sort_values('number_of_reviews', ascending=False).reset_index().head(10)

    df_aux01 = pd.merge(df_brooklyn, df_manhattan, how='outer')
    df_aux02 = pd.merge(df_aux01, df_queens, how='outer')
    df_aux03 = pd.merge(df_aux02, df_staten, how='outer')
    df2 = pd.merge(df_aux03, df_bronx, how='outer')

    nyc_map = folium.Map(location=[40.7128, -74.0060], zoom_start=10)
    for index, location_info in df2.iterrows():
        folium.Marker([location_info['latitude'],
                        location_info['longitude']],
                        popup=folium.Popup(f"Numero de reviews= {location_info['number_of_reviews']}", max_width=300)).add_to(nyc_map)
    
    folium_static(nyc_map, width=800, height=500)

    return None
#---------------------------------- CODE LOGIC STRUTURE -----------------------------------

#========================================================
# IMPORT DATASET
#========================================================
df = pd.read_csv('dataset/Data.csv')

#========================================================
# CLEAN DATA
#========================================================
df1 = clean_data( df )

#========================================================
# SET STREAMLIT PAGE WIDTH
#========================================================
st.set_page_config(page_title='Dashboard', page_icon='📊', layout='wide')

#========================================================
# PAGE LAYOUT
#========================================================
st.markdown('# 📊 Dashboard')

with st.container():
    st.markdown('## Métricas Gerais')
    col1, col2, col3 = st.columns(3)
    with col1:
        df2 = np.round(df1['price'].mean(), 2)
        st.metric(label='Valor Médio do aluguel', value=f'$ {df2}')
    
    with col2:
        df2 = df1['price'].max()
        st.metric(label='Aluguel mais caro', value=f'$ {df2}')
    
    with col3:
        df2 = np.std(df1['price']).round(2)
        st.metric(label='Desvio padrão do aluguel', value=f'$ {df2}')

st.markdown('''---''')

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('## Preço por região')
        fig = price_by_region( df1 )
        st.plotly_chart(fig)

    with col2:
        st.markdown('## Mapa - Top 10 mais avaliados por região')
        new_york_city_map( df1 )