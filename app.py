import streamlit as st
import pandas as pd
import preprocessor,helper
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
import numpy as np


df = pd.read_csv("athlete_events.csv")
region_df = pd.read_csv("noc_regions.csv")

df= preprocessor.preprocess(df,region_df)

st.sidebar.title("Olympics Analysis")
st.sidebar.image('https://static.vecteezy.com/system/resources/previews/037/899/703/non_2x/3d-olympic-rings-with-shadow-olympic-games-logo-illustration-free-vector.jpg')
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Overall Performance','Country-wise Analysis','Athlete-wise Analysis')
)
 

if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years, country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title('Overall Tally')
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title('Medal Tally in ' + str(selected_year) + ' Olympics')
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + ' Overall Performance')
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country +' Performance in ' + str(selected_year) + ' Olympics')
    st.table(medal_tally)



if user_menu == 'Overall Performance':
    editions = df['Year'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations =  df['region'].unique().shape[0]

    st.title("Top Stats")
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Atheletes")
        st.title(athletes)

    nations_over_time = helper.data_over_time(df,'region')
    fig = px.line(nations_over_time, x="Year", y="region")
    st.title("Participating Nations Over time")
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(df,'Event')
    fig = px.line(events_over_time, x="Year", y="Event")
    st.title("Events Over time")
    st.plotly_chart(fig)

    athletes_over_time = helper.data_over_time(df,'Name')
    fig = px.line(athletes_over_time, x="Year", y="Name")
    st.title("Athletes Over time")
    st.plotly_chart(fig)


    st.title("No of Events over time(Every Sport)")
    fig,ax = plt.subplots(figsize=(25,25))
    x = df.drop_duplicates(['Year','Sport','Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport',columns='Year', values='Event',aggfunc='count').fillna(0).astype('int'),annot=True)
    st.pyplot(fig)

    st.title("Most Successful Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')

    Selected_sport = st.selectbox('Select a Sport',sport_list)
    x= helper.most_successful(df,Selected_sport)
    st.table(x)


if user_menu == 'Country-wise Analysis':
    
    st.sidebar.title("Country-wise Analysis")
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    # country_list.insert(0,'Overall')

    Selected_country = st.sidebar.selectbox('Select a Country',country_list)

    country_df = helper.yearwise_medal_tally(df,Selected_country)
    fig = px.line(country_df, x='Year', y='Medal')
    st.title(Selected_country + ' Medal Tally over the years')
    st.plotly_chart(fig)

    st.title(Selected_country + ' excels in the following sports')
    pt = helper.country_event_heatmap(df, Selected_country)
    fig,ax = plt.subplots(figsize=(20,20))
    ax = sns.heatmap(pt,annot=True)
    st.pyplot(fig)

    st.title("Top 10 athletes of " + Selected_country)
    top10_df = helper.top_athletes_countrywise(df,Selected_country)
    st.table(top10_df)

if user_menu == 'Athlete-wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name','region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] =='Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] =='Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] =='Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1,x2,x3,x4],['Overall Age Distribution','Gold Medalist','Silver Medalist','Bronze Medalist'],show_hist=False,show_rug=False)
    fig.update_layout(width=1000, height=500) 
    st.title("Age Distribution")
    st.plotly_chart(fig)

    gold_df = athlete_df[athlete_df['Medal'] == 'Gold']

    fig = px.box(gold_df,y='Age',color='Sport',
        category_orders={'Sport': gold_df.groupby('Sport')['Age'].median().sort_values().index},
        width=1200,height=600)

    # Add space between boxes and adjust margins
    fig.update_layout(boxmode='group',boxgap=0)

    fig.update_xaxes(tickangle=45)

    st.title("Gold Medalist Age Distribution w.r.t sport")
    st.plotly_chart(fig)


    famous_sports = athlete_df['Sport'].unique()
    x = []
    label = []

    for sport in famous_sports:
        temp_df = athlete_df[(athlete_df['Sport'] == sport) & (athlete_df['Medal'] == 'Gold')]
        ages = temp_df['Age'].dropna()

        # Only keep if 3+ points AND not all the same
        if len(ages) >= 3 and np.std(ages) > 0:
            x.append(ages)
            label.append(sport)

    if len(x) > 1:
        fig = ff.create_distplot(x, label,show_hist=False,show_rug=False)
        fig.update_layout(
            xaxis_title='Age',yaxis_title='Density',
            width=6500,height=700,
            legend_title='Sports',
            template='plotly_white' )
       
    else:
        print(f"Not enough valid sports to plot. Only {len(x)} sport(s) passed filtering.")
        print("Sports included:", label)
    st.title("Gold Medalist Age Distribution w.r.t sport2")
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')

    st.title("Athetes Height vs Weight")
    Selected_sport = st.selectbox('Select a Sport',sport_list)
    temp_df = helper.weight_v_height(df,Selected_sport)
    fig,ax = plt.subplots()
    ax = sns.scatterplot(x= temp_df['Weight'],y= temp_df['Height'], hue=temp_df['Medal'],style=temp_df['Sex'],s=60)
    st.pyplot(fig)


    st.title("Men vs Women Participation Over the Years")
    final = helper.men_vs_women(df)
    fig = px.line(final,x='Year',y=['Male','Female'])
    fig.update_layout(width=1000, height=500) 
    st.plotly_chart(fig)

