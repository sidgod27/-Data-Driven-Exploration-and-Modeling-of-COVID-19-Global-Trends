
# Covid-19 Impacts Analysis
"""

# Imports
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import matplotlib.pyplot as plt


print('Imports complete')


# Data path: change this if your CSV is elsewhere
data_path = 'Covid19.Data.csv'

# Load the data
try:
    data = pd.read_csv(data_path)
    print('Loaded', data_path)
    display(data.head())
except FileNotFoundError:
    print(f"File not found: {data_path}. Please update `data_path` or upload the CSV to this folder.")
    raise

"""## Data Preparation

This section inspects the dataset, aggregates per-country metrics, and creates a summarized DataFrame similar to the original script.
"""

# Inspect counts per country
print(data['COUNTRY'].value_counts())

# Mode (as in original script)
print('Mode value for counts:', data['COUNTRY'].value_counts().mode())

# Create aggregated lists (keeping original logic)
code = data['CODE'].unique().tolist()
country = data['COUNTRY'].unique().tolist()
hdi = []
tc = []
td = []
sti = []
population = data['POP'].unique().tolist()
gdp = []

for i in country:
    hdi.append((data.loc[data['COUNTRY'] == i, 'HDI']).sum()/294)
    tc.append((data.loc[data['COUNTRY'] == i, 'TC']).sum())
    td.append((data.loc[data['COUNTRY'] == i, 'TD']).sum())
    sti.append((data.loc[data['COUNTRY'] == i, 'STI']).sum()/294)
    population.append((data.loc[data['COUNTRY'] == i, 'POP']).sum()/294)

aggregated_data = pd.DataFrame(list(zip(code, country, hdi, tc, td, sti, population)),
                               columns=["Country Code", "Country", "HDI",
                                        "Total Cases", "Total Deaths",
                                        "Stringency Index", "Population"])
print(aggregated_data.head())

# Sorting and selecting top 10

data = aggregated_data.sort_values(by=['Total Cases'], ascending=False)
print(data.head())

data = data.head(10)
print(data)

# Add GDP columns (hard-coded values from script)

data['GDP Before Covid'] = [65279.53, 8897.49, 2100.75,
                            11497.65, 7027.61, 9946.03,
                            29564.74, 6001.40, 6424.98, 42354.41]

data['GDP During Covid'] = [63543.58, 6796.84, 1900.71,
                            10126.72, 6126.87, 8346.70,
                            27057.16, 5090.72, 5332.77, 40284.64]
print(data)

# Plot: Countries with Highest Covid Cases
figure = px.bar(data, y='Total Cases', x='Country',
            title="Countries with Highest Covid Cases")
figure.show()

# Plot: Countries with Highest Deaths
figure = px.bar(data, y='Total Deaths', x='Country',
            title="Countries with Highest Deaths")
figure.show()

# Grouped bar: Total Cases vs Total Deaths
fig = go.Figure()
fig.add_trace(go.Bar(
    x=data['Country'],
    y=data['Total Cases'],
    name='Total Cases',
    marker_color='indianred'
))



fig.add_trace(go.Bar(
    x=data['Country'],
    y=data['Total Deaths'],
    name='Total Deaths',
    marker_color='lightsalmon'
))
fig.update_layout(barmode='group', xaxis_tickangle=-45)
fig.show()

# Percentage of Total Cases and Deaths (pie)
cases = data['Total Cases'].sum()
deceased = data['Total Deaths'].sum()
labels = ['Total Cases', 'Total Deaths']
values = [cases, deceased]
fig = px.pie(data, values=values, names=labels,
             title='Percentage of Total Cases and Deaths', hole=0.5)
fig.show()

# Death rate
death_rate = (data['Total Deaths'].sum() / data['Total Cases'].sum()) * 100
print('Death Rate =', death_rate)

# Stringency Index bar
fig = px.bar(data, x='Country', y='Total Cases',
             hover_data=['Population', 'Total Deaths'],
             color='Stringency Index', height=400,
             title= "Stringency Index during Covid-19")
fig.show()

# GDP per capita before Covid
fig = px.bar(data, x='Country', y='Total Cases',
             hover_data=['Population', 'Total Deaths'],
             color='GDP Before Covid', height=400,
             title="GDP Per Capita Before Covid-19")
fig.show()

# GDP per capita during Covid
fig = px.bar(data, x='Country', y='Total Cases',
             hover_data=['Population', 'Total Deaths'],
             color='GDP During Covid', height=400,
             title="GDP Per Capita During Covid-19")
fig.show()

# Grouped GDP comparison
fig = go.Figure()
fig.add_trace(go.Bar(
    x=data['Country'],
    y=data['GDP Before Covid'],
    name='GDP Per Capita Before Covid-19',
    marker_color='indianred'
))
fig.add_trace(go.Bar(
    x=data['Country'],
    y=data['GDP During Covid'],
    name='GDP Per Capita During Covid-19',
    marker_color='lightsalmon'
))
fig.update_layout(barmode='group', xaxis_tickangle=-45)
fig.show()

# HDI bar
fig = px.bar(data, x='Country', y='Total Cases',
             hover_data=['Population', 'Total Deaths'],
             color='HDI', height=400,
             title="Human Development Index during Covid-19")
fig.show()

# GDP Impact Analysis
# First, let's filter working_data to get top 10 countries by total cases
working_data = data.sort_values('Total Cases', ascending=False).head(10).copy()

# Now we can safely add the GDP data
working_data['GDP Before Covid'] = [65279.53, 8897.49, 2100.75,
                                  11497.65, 7027.61, 9946.03,
                                  29564.74, 6001.40, 6424.98, 42354.41]
working_data['GDP During Covid'] = [63543.58, 6796.84, 1900.71,
                                  10126.72, 6126.87, 8346.70,
                                  27057.16, 5090.72, 5332.77, 40284.64]

# Calculate GDP change
working_data['GDP Change'] = ((working_data['GDP During Covid'] - working_data['GDP Before Covid']) / working_data['GDP Before Covid']) * 100

# Sort by GDP impact and display results
gdp_impact = working_data.sort_values('GDP Change')[['Country', 'GDP Before Covid', 'GDP During Covid', 'GDP Change']]
gdp_impact['GDP Change'] = gdp_impact['GDP Change'].round(2)
print("\nGDP Impact Analysis (sorted by largest decline):")
print(gdp_impact)

# Create a waterfall chart of GDP changes
fig = go.Figure(go.Waterfall(
    name="GDP Change",
    orientation="v",
    measure=["relative"] * len(working_data),
    x=working_data['Country'],
    textposition="outside",
    text=[f"{x:.1f}%" for x in working_data['GDP Change']],
    y=working_data['GDP Change'],
    connector={"line":{"color":"rgb(63, 63, 63)"}},
))

fig.update_layout(
    title="GDP Change During COVID-19 (%)",
    showlegend=True,
    xaxis_title="Country",
    yaxis_title="GDP Change (%)"
)
fig.show()

# Calculate Case Fatality Rate (CFR) and other health metrics
working_data['Case Fatality Rate'] = (working_data['Total Deaths'] / working_data['Total Cases']) * 100
working_data['Cases per HDI point'] = working_data['Total Cases'] / working_data['HDI']

# Create summary statistics
health_metrics = working_data[['Country', 'Case Fatality Rate', 'HDI']]
print("\nHealth System Impact Analysis:")
print(health_metrics.sort_values('Case Fatality Rate', ascending=False))

# Visualize Case Fatality Rate vs HDI
fig = px.scatter(working_data,
                x='HDI',
                y='Case Fatality Rate',
                size='Total Cases',  # Bubble size represents total cases
                text='Country',
                title='Case Fatality Rate vs HDI (bubble size = total cases)',
                labels={'Case Fatality Rate': 'Case Fatality Rate (%)',
                       'HDI': 'Human Development Index'})
fig.show()

# Create a multi-metric comparison
fig = go.Figure()

# Normalize metrics for comparison
for metric in ['Case Fatality Rate', 'Stringency Index', 'HDI']:
    normalized = (working_data[metric] - working_data[metric].min()) / (working_data[metric].max() - working_data[metric].min()) * 100
    fig.add_trace(go.Bar(name=metric, x=working_data['Country'], y=normalized))

fig.update_layout(barmode='group',
                 title='Multi-metric Comparison (Normalized Values)',
                 xaxis_tickangle=-45)
fig.show()

import pandas as pd

# Corrected sample data with equal lengths for each list
working_data = pd.DataFrame({
    'Country': [
        'USA', 'Brazil', 'India', 'Russia', 'UK', 'France', 'Italy', 'Spain', 'Germany', 'Argentina',
        'Canada', 'Mexico', 'China', 'Japan', 'Australia', 'South Africa', 'Saudi Arabia', 'Turkey',
        'South Korea', 'Netherlands', 'Colombia', 'Peru', 'Chile', 'Poland', 'Ukraine', 'Sweden', 'Belgium',
        'Austria', 'Philippines', 'Thailand', 'Vietnam', 'Malaysia', 'New Zealand', 'Egypt', 'Nigeria',
        'Kenya', 'Morocco', 'UAE', 'Qatar', 'Oman'
    ],
    'Total Cases': [
        50000000, 30000000, 40000000, 10000000, 15000000, 12000000, 9000000, 8000000, 10000000, 7000000,
        6000000, 9000000, 12000000, 8000000, 3000000, 5000000, 4000000, 7000000, 5000000, 6000000,
        6000000, 5000000, 4000000, 3500000, 3000000, 2800000, 2700000, 2600000, 2500000, 2400000, 2300000, 2200000,
        2100000, 2000000, 1950000, 1900000, 1850000, 1800000, 1700000, 1600000
    ],
    'Total Deaths': [
        800000, 600000, 500000, 200000, 150000, 130000, 90000, 80000, 110000, 60000,
        50000, 80000, 90000, 40000, 25000, 70000, 40000, 60000, 32000, 35000,
        90000, 70000, 65000, 58000, 60000, 55000, 50000, 48000, 46000, 44000, 42000, 40000,
        38000, 36000, 34000, 32000, 30000, 28000, 27000, 26000
    ]
})

region_mapping = {
    'USA': 'North America', 'Canada': 'North America', 'Mexico': 'North America',
    'Brazil': 'South America', 'Argentina': 'South America', 'Colombia': 'South America', 'Peru': 'South America', 'Chile': 'South America',
    'India': 'Asia', 'China': 'Asia', 'Japan': 'Asia', 'South Korea': 'Asia', 'Philippines': 'Asia', 'Thailand': 'Asia', 'Vietnam': 'Asia', 'Malaysia': 'Asia', 'New Zealand': 'Oceania', 'Oman': 'Middle East',
    'Russia': 'Europe', 'UK': 'Europe', 'France': 'Europe', 'Italy': 'Europe', 'Spain': 'Europe', 'Germany': 'Europe', 'Poland': 'Europe', 'Ukraine': 'Europe', 'Sweden': 'Europe', 'Belgium': 'Europe', 'Austria': 'Europe', 'Netherlands': 'Europe',
    'South Africa': 'Africa', 'Egypt': 'Africa', 'Nigeria': 'Africa', 'Kenya': 'Africa', 'Morocco': 'Africa',
    'Saudi Arabia': 'Middle East', 'Turkey': 'Middle East', 'UAE': 'Middle East', 'Qatar': 'Middle East'
}

# Map countries to regions
working_data['Region'] = working_data['Country'].map(region_mapping)

# Calculate fatality rate
working_data['Fatality Rate'] = working_data['Total Deaths'] / working_data['Total Cases']

# Sort and take top 10 countries with highest fatality rate from each region
top_10_per_region = working_data.sort_values('Fatality Rate', ascending=False).groupby('Region').head(10).reset_index(drop=True)

top_10_per_region[['Country', 'Region', 'Total Cases', 'Total Deaths', 'Fatality Rate']]

from matplotlib import pyplot as plt
import seaborn as sns
figsize = (12, 1.2 * len(_df_11['Region'].unique()))
plt.figure(figsize=figsize)
sns.violinplot(_df_11, x='Fatality Rate', y='Region', inner='stick', palette='Dark2')
sns.despine(top=True, right=True, bottom=True, left=True)
