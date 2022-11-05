from sre_parse import State
import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
import folium
from streamlit_folium import st_folium

APP_TITLE = 'Diet Preference Survey'
APP_SUB_TITLE = 'Source: Social Determinants of Health Data'
st.set_page_config(layout='wide', initial_sidebar_state='expanded')

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
st.sidebar.header('Dashboard `version 1.1`')
# import the data set
df = pd.read_csv('midterm.csv')
#st.write(df)

st.sidebar.header("Pick two variables for your dashboard")
x_val= st.sidebar.selectbox("Pick a type of diet", ('DIET_CAGEFREE_EGGS', 'DIET_FAKE_MEAT_ALT', 'DIET_FREERANGE_CHICKEN', 'DIET_GRASSFED_BEEF', 'DIET_VEGETARIAN', 'DIET_VEGAN'))
y_val= st.sidebar.selectbox("Pick your y-axis", ('STATE', 'CITY'))

#State
#average_state = round(df_selection["Rating"].mean(), 1)
average_score = df.groupby(by=[y_val]).mean()[[x_val]].sort_values(by=x_val, ascending=False)
#st.write(average_score)
#max_score=st.write(average_score.max()[[x_val]])
#st.write(average_score.columns)
#df = pd.DataFrame(average_score)



st.title(APP_TITLE)
st.caption(APP_SUB_TITLE)   


#Columns
# create two columns for charts
fig_col1, fig_col2 = st.columns(2)

with fig_col1:
    #Map
        st.markdown("### Diet preference by state")
        st.write(f"Average score of {x_val} per State")
        #Map
        map = folium.Map(location=[38, -96.5], zoom_start=3, scrollWheelzoom=False, tiles='CartoDB positron')

        choropleth = folium.Choropleth(
        geo_data = 'us-state-boundaries.geojson',
        data=df,
        columns=('STATE', x_val),
        key_on='feature.properties.stusab',
        line_opacity=0.8,
        highlight=True

        )
        choropleth.geojson.add_to(map)
        choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(['name'], labels=False)
        )

        st_map = st_folium(map, width=350, height=200)

    # Education bar
        st.markdown("### Respondent's level of education")
        score=df.groupby(['AIQ_EDUCATION_V2'])[x_val].mean().reset_index().sort_values(by=x_val, ascending=False)
        st.write(f"Relation between {y_val} and {x_val} score")
        bar = alt.Chart(score).mark_bar().encode(
        alt.X(x_val, title=f"{x_val} score"),
        alt.Y('AIQ_EDUCATION_V2', title="Level of Education", sort='-x')
        )
        st.altair_chart(bar, use_container_width=True)
   
with fig_col2:
    # States bar
        st.markdown("### Top 20 states")
        st.write(f"List of top 20 {y_val} by {x_val} score")
        score=df.groupby([y_val])[x_val].mean().reset_index().sort_values(by=x_val, ascending=False)[:20]
     
        bar = alt.Chart(score).mark_bar().encode(
        alt.X(x_val, title=f"{x_val} score"),
        alt.Y(y_val, title=f"{y_val}", sort='-x')
        )
        st.altair_chart(bar, use_container_width=True)
