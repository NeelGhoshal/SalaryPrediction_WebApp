import streamlit as st
import pickle
import numpy as np


#Reference JupterNB for code snippets applied here
def load_model():
    with open('saved_steps.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

data = load_model()

regressor = data["model"]
le_country = data["le_country"]
le_education = data["le_education"]

#Creating the prediction page
def show_predict_page():
    st.title("Software Developer Salary Prediction")

    st.write("""### We need some information to predict the salary""")  #Content here is considered in a markdown file syntax

    countries = (
        "United States of America",
        "Germany",
        "United Kingdom of Great Britain and Northern Ireland",
        "India",
        "Canada",
        "France",
        "Brazil",
        "Spain",
        "Netherlands",
        "Australia",
        "Italy",
        "Poland",
        "Sweden",
        "Russian Federation",
        "Switzerland"                                          
    )

    education = (
        'Less than a Bachelors',
        'Bachelor’s degree',
        'Master’s degree',
        'Post grad'
    )

    country = st.selectbox("Country", countries) #Selectbox created on the web page for selecting the variable 'country'
    education = st.selectbox("Education Level", education) 
    experience = st.slider("Years of Experience", 0,50,3) #title, minVal, maxVal, startVal

    ok = st.button("Calculate Salary") #Creating a button
    if ok:
        X = np.array([[country, education, experience]])
        X[:, 0] = le_country.transform(X[:,0]) #apply label_encoder to entire array of 1st column (in the 2D overall array)
        X[:, 1] = le_education.transform(X[:,1]) #similar to above (label encoding)
        X = X.astype(float)

        salary = regressor.predict(X)
        st.subheader(f"The estimated salary is ${salary[0]:.2f}") #Display value
