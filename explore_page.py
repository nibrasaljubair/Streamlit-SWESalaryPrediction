import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def shorten_categories(categories, cutoff):
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = 'Other'
    return categorical_map

def clean_experience(x):
    if x == 'More than 50 years':
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

@st.cache_data
def load_data():
    df = pd.read_csv("Survey_results_public.csv")
    df = df[["Country", "EdLevel", "YearsCodePro", "Employment", "ConvertedCompYearly"]]
    df = df.rename({"ConvertedCompYearly": "Salary"}, axis=1)
    df = df[df["Salary"].notnull()]
    df = df.dropna()
    df = df[df["Employment"] == "Employed, full-time"]
    df = df.drop("Employment", axis=1)

    country_map = shorten_categories(df.Country.value_counts(), 400)
    df['Country'] = df['Country'].map(country_map)
    df = df[df["Salary"] <= 250000]
    df = df[df["Salary"] >= 10000]
    df = df[df['Country'] != 'Other']

    df["YearsCodePro"] = df["YearsCodePro"].apply(clean_experience)
    df["EdLevel"] = df["EdLevel"].apply(clean_education) 

    return df    

df = load_data()

def show_explore_page():
    st.title("💼 Explore Software Engineer Salaries")
    st.markdown("""
        ### Data Overview  
        This dashboard explores salary trends from the Stack Overflow Developer Survey.  
        Gain insights into how salaries vary by **country**, **years of experience**, and **education level**.  
    """)

  
    st.markdown("### 🌍 Number of Responses by Country")
    data = df["Country"].value_counts()
    fig1, ax1 = plt.subplots(figsize=(6, 6))
    ax1.pie(data, labels=data.index, autopct="%1.1f%%", shadow=False, startangle=90, textprops={'fontsize': 9})
    ax1.axis("equal")
    st.pyplot(fig1)


    st.markdown("### 💵 Mean Salary by Country")
    country_salary = df.groupby("Country")["Salary"].mean().sort_values(ascending=True)
    st.bar_chart(country_salary)


    st.markdown("### 📈 Mean Salary by Years of Professional Experience")
    exp_salary = df.groupby("YearsCodePro")["Salary"].mean().sort_values(ascending=True)
    st.line_chart(exp_salary)

##show_explore_page()
