import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Title page
st.set_page_config(page_title="Air Quality from Nongzhanguan Analysis")


# Load dataset
data = pd.read_csv("data/PRSA_Data_Nongzhanguan_20130301-20170228.csv")

# Title of the dashboard
st.title("Air Quality Analysis Dashboard: Nongzhanguan Station")


# Description
st.write(
    "This dashboard presents an interactive analysis of air quality data, with a specific focus on PM10 levels and their correlation with different weather conditions."
)

st.markdown(
    """
### Project Overview
This dashboard provides an analysis of air quality data, specifically emphasizing PM10 levels, 
obtained from the Nongzhanguan station. The objective of the project is to reveal patterns, seasonal fluctuations, 
and the influence of various weather conditions on air quality. The findings from this analysis hold significance for 
environmental research and the surveillance of public health."""
)

st.subheader("Dataset Overview")
st.write(
    "This Dataset contains:",
    data.shape[0],
    "rows and",
    data.shape[1],
    "columns from March 2013 to February 2017.",
)
st.write(data.describe())


# Adding a sidebar for interactive inputs
st.sidebar.header("Choose time period")

# Let users select a year and month to view data
selected_year = st.sidebar.selectbox("Select Year", sorted(list(data["year"].unique())))

if selected_year == 2013:
    selected_month = st.sidebar.selectbox(
        "Select Month",
        sorted(list(data[data["year"] == selected_year]["month"].unique()))[0:],
    )
elif selected_year == 2017:
    selected_month = st.sidebar.selectbox(
        "Select Month",
        sorted(list(data[data["year"] == selected_year]["month"].unique()))[:12],
    )
else:
    selected_month = st.sidebar.selectbox(
        "Select Month",
        sorted(list(data[data["year"] == selected_year]["month"].unique())),
    )

# Filter data based on the selected year and month
data_filtered = data[
    (data["year"] == selected_year) & (data["month"] == selected_month)
].copy()

# Clear button
if st.sidebar.button("Clear"):
    data_filtered = data.copy()

# Displaying data statistics
st.subheader("Data Overview for Selected Period")
st.write(data_filtered.describe())


# Visualizing PM10 levels
st.subheader("Daily PM10 Level")

# Combine day, month, and year columns into a 'date' column
data_filtered["date"] = pd.to_datetime(data_filtered[["year", "month", "day"]])

# Calculate daily average PM10 levels
daily_avg_pm10 = data_filtered.groupby("date")["PM10"].mean()

# Plotting the line chart
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(daily_avg_pm10, marker="o", linestyle="-", color="b")

# Adding labels and title
ax.set_xlabel("Date")
ax.set_ylabel("Average PM10 Concentration")

# Display the plot
plt.grid(True)
plt.tight_layout()
plt.show()


st.pyplot(fig)

# Calculate all time average PM10 levels
all_time_avg_pm10 = data["PM10"].mean()

# Calculate this month average PM10 levels
this_month_avg_pm10 = data_filtered["PM10"].mean()
st.subheader("Yearly Pollutant Distribution")

# Filter numeric columns
numeric_columns = data.select_dtypes(include=np.number).columns

# Group data by year and calculate average pollutant levels
yearly_avg_pollutants = data.groupby("year")[numeric_columns].mean()

# Let users select the pollutants to visualize
selected_pollutant = st.selectbox(
    "Select Pollutant",
    list(["SO2", "NO2", "CO", "O3", "TEMP", "PRES", "DWP", "RAIN", "WSPM"]),
    index=0,
)

# Filter data based on selected pollutant
selected_pollutant_data = yearly_avg_pollutants[selected_pollutant]

# Plotting the line chart
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(
    selected_pollutant_data.index,
    selected_pollutant_data,
    marker="o",
    linestyle="-",
    label=selected_pollutant,
)

# Adding labels and title
ax.set_xlabel("Year")
ax.set_ylabel("Average Pollutant Concentration")
ax.legend()

# Display the plot
plt.grid(True)
plt.tight_layout()
st.pyplot(fig)


# Display the Monthly Average PM10 levels
st.subheader("Monthly Average PM10 Concentration")


# Compare this month average to all time average
st.write("This month average PM10 concentration:", this_month_avg_pm10)
st.write("All time average PM10 concentration:", all_time_avg_pm10)

fig, ax = plt.subplots(figsize=(6, 1))
ax.barh(
    ["Current Period", "All Time"],
    [this_month_avg_pm10, all_time_avg_pm10],
    color=["blue", "green"],
)

# Calculate the percentage difference
percentage_diff = ((this_month_avg_pm10 - all_time_avg_pm10) / all_time_avg_pm10) * 100

# Annotate the percentage difference
if percentage_diff > 0:
    percentage_diff_text = f"+{percentage_diff:.2f}%"
else:
    percentage_diff_text = f"{percentage_diff:.2f}%"

ax.annotate(
    percentage_diff_text,
    xy=(this_month_avg_pm10, 0),
    xytext=(10, 0),
    textcoords="offset points",
    va="center",
    color="black",
    fontweight="bold",
)
st.pyplot(fig)


# Correlation Heatmap
st.subheader("Correlation Heatmap")
selected_columns = st.multiselect(
    "Select Columns for Correlation",
    list(
        [
            "PM10",
            "PM2.5",
            "SO2",
            "NO2",
            "CO",
            "O3",
            "TEMP",
            "PRES",
            "DWP",
            "RAIN",
            "WSPM",
            "wd",
        ]
    ),
    default=["PM10", "NO2", "CO", "SO2", "TEMP"],
)
corr = data[selected_columns].corr()
fig, ax = plt.subplots()
sns.heatmap(corr, annot=True, ax=ax)

st.pyplot(fig)


st.subheader("Conclusion")

tab1, tab2 = st.tabs(["Conclusion 1", "Conclusion 2"])
with tab1:
    st.text_area(
        "",
        "The air quality at Aotizhongxin has shown fluctuations from year to year. Both PM2.5 and PM10 concentration levels exhibit a varying trend. In 2016, the air quality graph indicates an overall increase with lower concentration levels. However, over time, these levels exhibit a random pattern, tending to decrease based on environmental factors.",
        disabled=True,
        height=130,
        label_visibility="collapsed",
    )
with tab2:
    st.text_area(
        "",
        "The provided analysis indicates that NO2 is the weather variable that correlates the most with PM10 levels. This strong positive correlation is supported by the shared sources of both pollutants, including vehicle emissions, industrial processes, and combustion of various fuels such as fossil fuels and biomass.",
        disabled=True,
        height=130,
        label_visibility="collapsed",
    )

with st.sidebar:
    st.subheader("About the Author")
    st.markdown("**Name**: Naoby Prawira")
    st.markdown("**Email**: naobyprawira8@gmail.com")
    st.markdown(
        "**Dicoding ID**: [naobyprawira](https://www.dicoding.com/users/naobyprawira/)"
    )
