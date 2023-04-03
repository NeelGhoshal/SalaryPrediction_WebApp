import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

#Refer JupyterNB for below functionalities
def shorten_categories(categories, cutoff): #'categories' implies the value counts and the cutoff is a integer
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = 'Other'
    return categorical_map

def clean_experience(x):
    if x ==  'More than 50 years':
        return 50
    if x == 'Less than 1 year':
        return 0.5
    return float(x)

def clean_education(x):
    if 'Bachelor’s degree' in x:
        return 'Bachelor’s degree'
    if 'Master’s degree' in x:
        return 'Master’s degree'
    if 'Professional degree' in x or 'Other doctoral' in x:
        return 'Post grad'
    return 'Less than a Bachelors'

#load data
@st.cache_data  #statement to cache the below code so as to not rerun the entire script at every reload and just cache it once and allow it to be available indefinitely
def load_data():
    df = df = pd.read_csv("Stackoverflow_data.csv")
    df = df[["Country", "EdLevel", "YearsCodePro", "Employment", "ConvertedCompYearly"]]
    # df = df.rename({"ConvertedCompYearly": "Salary"}, axis=1)
    df = df[df["ConvertedCompYearly"].notnull()]
    df = df.dropna()
    df = df[df["Employment"] == "Employed, full-time"]
    df = df.drop("Employment", axis=1)
    country_map = shorten_categories(df.Country.value_counts(), 400)
    df['Country'] = df['Country'].map(country_map)
    df = df[df["ConvertedCompYearly"] <= 250000]
    df = df[df["ConvertedCompYearly"] >= 10000]
    df = df[df['Country'] != 'Other']
    df['YearsCodePro'] = df['YearsCodePro'].apply(clean_experience)
    df['EdLevel'] = df['EdLevel'].apply(clean_education)
    df = df.rename({"ConvertedCompYearly": "Salary"}, axis=1) #defered to end due to error resolving
    return df #Returning clean dataframe

df = load_data()

def show_explore_page():
    st.title("Explore Software Developer Salaries")

    st.write("""
    ### Stack Overflow Developer Survey Info
    """)

    data = df["Country"].value_counts()

    #create graph
    fig1, ax1 = plt.subplots()
    ax1.pie(data, labels=data.index, shadow=True, startangle=90)
    ax1.axis("equal") #ensures pie is drwan as a circle

    st.write("""#### Number of Data from different countries""")
    st.pyplot(fig1)

    st.write("""#### Mean Salary Based On the Country""")
    data = df.groupby(["Country"])["Salary"].mean().sort_values(ascending=True)
    st.bar_chart(data)

    st.write("""#### Mean Salary based on the Experience""")
    data = df.groupby(["YearsCodePro"])["Salary"].mean().sort_values(ascending=True)
    st.line_chart(data)