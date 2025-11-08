import streamlit as st
import pandas as pd
import preprocessor, helper
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
import numpy as np

# Set page config for wider layout
st.set_page_config(page_title="Olympics Data Analysis", layout="wide")

# Load data once
@st.cache_data
def load_data():
    df = pd.read_csv("athlete_events.csv")
    region_df = pd.read_csv("noc_regions.csv")
    return preprocessor.preprocess(df, region_df)

df = load_data()

# Sidebar
st.sidebar.title("🏆 Olympics Analysis")
st.sidebar.image('https://static.vecteezy.com/system/resources/previews/037/899/703/non_2x/3d-olympic-rings-with-shadow-olympic-games-logo-illustration-free-vector.jpg',width=250)
st.sidebar.markdown("Olympics data from 1896 to 2016.")

user_menu = st.sidebar.radio( 'Select an Option',
    ('Medal Tally', 'Overall Performance', 'Country-wise Analysis', 'Athlete-wise Analysis'))

# 1️⃣ Medal Tally Section
if user_menu == 'Medal Tally':
    st.sidebar.header("🏅 Medal Tally")
    years, country = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)

    # Titles
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title('🏅 Overall Medal Tally')
    elif selected_year != 'Overall' and selected_country == 'Overall':
        st.title(f'🏅 Medal Tally in {selected_year} Olympics')
    elif selected_year == 'Overall' and selected_country != 'Overall':
        st.title(f'🏅 {selected_country} Overall Performance')
    else:
        st.title(f'🏅 {selected_country} Performance in {selected_year} Olympics')

    # Simple readable table (no gradients)
    styled_df = medal_tally.style.set_properties(
        **{'color': 'white',
            'background-color': '#1E1E1E',
            'font-size': '14px',
            'text-align': 'center',
            'border': '1px solid #333'})
    st.dataframe(styled_df, use_container_width=True)

    # CSV download
    csv = medal_tally.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Medal Tally as CSV", csv, "medal_tally.csv", "text/csv")

# 2️⃣ Overall Performance Section
elif user_menu == 'Overall Performance':
    editions = df['Year'].nunique()
    events = df['Event'].nunique()
    cities = df['City'].nunique()
    sports = df['Sport'].nunique()
    athletes = df['Name'].nunique()
    nations = df['region'].nunique()

    st.header("🏅 Top Stats")
    col1, col2, col3 = st.columns(3)
    col1.metric("Editions", editions)
    col2.metric("Hosts", cities)
    col3.metric("Sports", sports)
    col1, col2, col3 = st.columns(3)
    col1.metric("Events", events)
    col2.metric("Nations", nations)
    col3.metric("Athletes", athletes)

    nations_over_time = helper.data_over_time(df, 'region')
    with st.expander("📈 Participating Nations Over Time"):
        fig = px.line(nations_over_time, x="Year", y="region", template='plotly_dark')
        st.plotly_chart(fig, use_container_width=True)

    events_over_time = helper.data_over_time(df, 'Event')
    with st.expander("📊 Events Over Time"):
        fig = px.line(events_over_time, x="Year", y="Event", template='plotly_dark')
        st.plotly_chart(fig, use_container_width=True)

    athletes_over_time = helper.data_over_time(df, 'Name')
    with st.expander("👟 Athletes Over Time"):
        fig = px.line(athletes_over_time, x="Year", y="Name", template='plotly_dark')
        st.plotly_chart(fig, use_container_width=True)

    # Loading spinner added
    st.header("No. of Events Over Time (per Sport)")
    with st.spinner("Loading heatmap..."):
        with st.expander("Show Heatmap of Events by Sport and Year"):
            fig, ax = plt.subplots(figsize=(15, 15))
            x = df.drop_duplicates(['Year', 'Sport', 'Event'])
            pt = x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype(int)
            sns.heatmap(pt, annot=True, fmt='d', cmap='YlGnBu', ax=ax)
            plt.title("Heatmap: Number of Events per Sport Over Years", fontsize=16, color='white')
            st.pyplot(fig)

    st.header("Most Successful Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    Selected_sport = st.selectbox('Select a Sport', sport_list)
    x = helper.most_successful(df, Selected_sport)
    st.dataframe(x.style.set_properties(**{'color': 'white', 'font-size': '14px'}), use_container_width=True)

# 3️⃣ Country-wise Analysis Section
elif user_menu == 'Country-wise Analysis':
    st.sidebar.title("Country-wise Analysis")
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    Selected_country = st.sidebar.selectbox('Select a Country', country_list)

    country_df = helper.yearwise_medal_tally(df, Selected_country)
    fig = px.line(country_df, x='Year', y='Medal', template='plotly_dark')
    st.title(f"{Selected_country} Medal Tally over the years")
    st.plotly_chart(fig, use_container_width=True)

    st.title(f"{Selected_country} Excels in the Following Sports")
    pt = helper.country_event_heatmap(df, Selected_country)

    # Handle float format error for heatmap
    fmt_type = '.0f' if np.allclose(pt.values, pt.values.astype(int)) else '.1f'

    fig, ax = plt.subplots(figsize=(18, 18))
    sns.heatmap(pt, annot=True, fmt=fmt_type, cmap='YlGnBu', ax=ax)
    plt.title(f"Heatmap: {Selected_country} Medal Counts by Sport and Year", fontsize=16, color='white')
    st.pyplot(fig)

    st.title(f"Top 10 Athletes of {Selected_country}")
    top10_df = helper.top_athletes_countrywise(df, Selected_country)
    st.dataframe(top10_df.style.set_properties(**{'color': 'white', 'font-size': '14px'}), use_container_width=True)

# 4️⃣ Athlete-wise Analysis Section
elif user_menu == 'Athlete-wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    # --- Age Distribution of Athletes ---
    with st.spinner("Loading Age Distribution..."):
        x1 = athlete_df['Age'].dropna()
        x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
        x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
        x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

        fig = ff.create_distplot([x1, x2, x3, x4],['Overall', 'Gold', 'Silver', 'Bronze'],show_hist=False, show_rug=False)
        fig.update_layout(
            width=1000, height=500,
            template='plotly_dark',
            title_text="Age Distribution of Athletes",
            title_font=dict(size=32),
            legend=dict(font=dict(size=12)))
        st.plotly_chart(fig, use_container_width=True)

    # --- Gold Medalist Age Distribution by Sport ---
    with st.spinner("Loading Gold Medalist Age Distribution..."):
        gold_df = athlete_df[athlete_df['Medal'] == 'Gold']
        fig = px.box(
            gold_df, y='Age', color='Sport',
            category_orders={'Sport': gold_df.groupby('Sport')['Age'].median().sort_values().index},
            width=1200, height=600,
            template='plotly_dark')

        # Add better layout with y-axis label and tick formatting
        fig.update_layout(
            boxmode='group', boxgap=0.3,
            yaxis_title="Age of Gold Medalists",
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.2)', tickfont=dict(color='white')),
            title=dict(text="Gold Medalist Age Distribution by Sport", font=dict(size=32)),
            legend_title_text='Sport',
            legend=dict(font=dict(size=12)))
        st.plotly_chart(fig, use_container_width=True)

    # --- Athletes Height vs Weight ---
    st.header("Athletes Height vs Weight")

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    Selected_sport = st.selectbox('Select a Sport', sport_list)

    temp_df = helper.weight_v_height(df, Selected_sport)

    with st.spinner("Loading Height vs Weight scatterplot..."):
        fig, ax = plt.subplots(figsize=(10, 6), facecolor="#0E1117")  # Dark background
        ax.set_facecolor("#0E1117")

        # ✅ More contrast between medal colors
        medal_palette = {
            'Gold': '#FFD700',   # Bright gold
            'Silver': '#C0C0C0', # Shiny silver
            'Bronze': '#CD7F32', # Deep bronze
            'No Medal': '#2a7abd'}

        sns.scatterplot(x=temp_df['Weight'], y=temp_df['Height'],hue=temp_df['Medal'], style=temp_df['Sex'],s=60, palette=medal_palette, ax=ax)

        plt.title("Athletes Height vs Weight", fontsize=16, color='white')
        plt.xlabel("Weight (kg)", fontsize=14, color='white')
        plt.ylabel("Height (cm)", fontsize=14, color='white')

        # Make axis tick values visible
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')

        # Improve legend appearance
        legend = plt.legend(title='Medal / Sex', fontsize=10, facecolor="#0E1117", edgecolor="none", labelcolor='white')
        plt.setp(legend.get_title(), color='white')
        plt.setp(legend.get_texts(), color='white')

        plt.grid(True, color='gray', linestyle='--', alpha=0.3)
        st.pyplot(fig)

    # --- Men vs Women Participation Over the Years ---
    st.header("Men vs Women Participation Over the Years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x='Year', y=['Male', 'Female'], template='plotly_dark')
    fig.update_layout(
        title="Men vs Women Participation Over the Years",
        xaxis_title="Year",
        yaxis_title="Number of Athletes",
        legend_title_text='Gender',
        title_font=dict(size=18))
    st.plotly_chart(fig, use_container_width=True)
