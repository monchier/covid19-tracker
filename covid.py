import streamlit as st
import pandas as pd
import altair as alt

st.title("Track Covid-19 over Time")

URL = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv"
data = pd.read_csv(URL)
st.markdown("Whole dataset from https://github.com/CSSEGISandData/COVID-19:")
st.write(data)

regions = data["Country/Region"].unique()
region = st.selectbox("Select a Country/Region", regions)
data = data[data["Country/Region"] == region]

st.markdown("Filtered by Country/Region:")
st.write(data)

search_value = st.text_input("Search Province/State")
include_na = st.checkbox("Include NA", True)
data = data[data["Province/State"].str.contains(search_value).fillna(include_na)]

st.markdown("Filtered by Province/State search:")
st.write(data)

data = data.iloc[:, 4:]
data = data.agg("sum").reset_index()
#st.write(data)
#data = data.groupby("Country/Region").sum().reset_index()
#data = data.T.reset_index()
data.columns = ['day', 'value']

st.markdown("### Total Confirmed Cases")
chart = (
    alt.Chart(data)
    .mark_line()
    .encode(
        y="value",
        x="day:T",
        #y=alt.Y("Gross Agricultural Product ($B):Q", stack=None),
        #color="Region:N",
    )
)
st.altair_chart(chart, use_container_width=True)

st.markdown("### Diff")
data["value"] = data["value"].diff()
st.write(data)
chart = (
    alt.Chart(data)
    .mark_line()
    .encode(
        y="value",
        x="day:T",
        #y=alt.Y("Gross Agricultural Product ($B):Q", stack=None),
        #color="Region:N",
    )
)
st.altair_chart(chart, use_container_width=True)

