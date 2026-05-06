
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Film Dashboard", page_icon="🎬", layout="wide")

data = {
    "Title": ["Dream City","Silent Ocean","Neon Runner","The Last Letter","Moonlight Code","Golden Hour","Broken Crown","Summer Signal"],
    "Genre": ["Drama","Thriller","Sci-Fi","Romance","Sci-Fi","Drama","Fantasy","Romance"],
    "Production Budget": [12000000,8500000,30000000,5000000,18000000,7000000,25000000,4000000],
    "Box Office Revenue": [45000000,15000000,76000000,12000000,14000000,22000000,31000000,9500000],
    "Director": ["Anna Kim","James Lee","Mina Park","David Choi","Sara Moon","Kevin Han","Lina Jung","Eric Kwon"],
    "Release Year": [2021,2020,2023,2019,2024,2022,2023,2021],
    "Rating": [8.2,7.4,8.8,7.9,6.8,8.0,7.1,7.6],
    "Production Status": ["Released","Released","Released","Released","Post-production","Released","Released","In Production"]
}

df = pd.DataFrame(data)
df["ROI (%)"] = ((df["Box Office Revenue"] - df["Production Budget"]) / df["Production Budget"] * 100).round(2)
df["Profit"] = df["Box Office Revenue"] - df["Production Budget"]

st.title("🎬 Film Production Dashboard")

# Sidebar
st.sidebar.header("Filters")
genre = st.sidebar.multiselect("Genre", df["Genre"].unique(), default=df["Genre"].unique())
year = st.sidebar.slider("Year", int(df["Release Year"].min()), int(df["Release Year"].max()),
                         (int(df["Release Year"].min()), int(df["Release Year"].max())))
status = st.sidebar.multiselect("Status", df["Production Status"].unique(), default=df["Production Status"].unique())
search = st.sidebar.text_input("Search")

filtered = df[
    (df["Genre"].isin(genre)) &
    (df["Release Year"].between(year[0], year[1])) &
    (df["Production Status"].isin(status))
]

if search:
    filtered = filtered[
        filtered["Title"].str.contains(search, case=False) |
        filtered["Director"].str.contains(search, case=False)
    ]

# Metrics
col1,col2,col3,col4 = st.columns(4)
col1.metric("Total Budget", f"${filtered['Production Budget'].sum():,}")
col2.metric("Total Revenue", f"${filtered['Box Office Revenue'].sum():,}")
col3.metric("Avg ROI", f"{filtered['ROI (%)'].mean():.2f}%")
col4.metric("Top Movie", filtered.loc[filtered["Box Office Revenue"].idxmax(),"Title"] if not filtered.empty else "N/A")

# Table
st.subheader("Film Data")
st.dataframe(filtered)

# Bar Chart
st.subheader("Budget vs Revenue")
bar = px.bar(filtered, x="Title", y=["Production Budget","Box Office Revenue"], barmode="group")
st.plotly_chart(bar, use_container_width=True)

# Pie Chart
st.subheader("Genre Distribution")
pie = px.pie(filtered, names="Genre")
st.plotly_chart(pie, use_container_width=True)
