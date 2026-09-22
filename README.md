# PaySprint FinTech Analysis: Alternative Credit Scoring Engine

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-Data_Manipulation-150458.svg)](https://pandas.pydata.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B.svg)](https://streamlit.io/)

## 📌 Project Overview
PaySprint is a digital lending platform experiencing a high volume of loan applications. However, despite strong demand, a significant portion of applicants were being auto-rejected by the traditional underwriting system. 

The goal of this project was to conduct an end-to-end **Exploratory Data Analysis (EDA)** on 15 months of loan data (7,000+ records) to uncover the root cause of these rejections and propose a data-driven product solution to capture lost revenue safely.

## ⚠️ The Problem: The Gig Economy Gap
Our analysis identified a massive revenue bottleneck:
* **Gig workers faced a disproportionate 40.3% rejection rate** compared to just 29.5% for salaried workers.
* The primary reasons for rejection were traditional metrics: **"Thin credit file"** and **"Low credit score."**
* However, when evaluating the gig workers who *did* receive loans, their **default rate was highly manageable at 5.2%**.

PaySprint was effectively turning away a highly profitable, creditworthy demographic simply because traditional bureau scoring models are designed for salaried workers, not the modern gig economy.

## 💡 The Solution: "SprintScore"
To capture this underserved market, we designed the product strategy for **SprintScore**—an alternative credit-scoring engine integrated into the PaySprint app. 

Instead of relying purely on archaic CIBIL/bureau scores, SprintScore evaluates thin-file applicants using alternative digital markers (e.g., app session engagement, KYC success, device data, and micro-income consistency). This strategy aims to:
1. Safely increase approval rates for gig workers by ~15%.
2. Acquire thousands of new customers at **$0 Customer Acquisition Cost (CAC)** by re-engaging historically rejected applicants.

## 📂 Repository Contents
* **`Group4_Analysis.ipynb`**: The core Jupyter Notebook containing the data cleaning pipeline and Exploratory Data Analysis.
* **`dashboard.py`**: An interactive Python (Streamlit) dashboard built to track Rejection Rates vs. Default Rates across employment segments.
* **`Group4_Cleaned.csv`**: The high-fidelity dataset post-cleaning (handling structural nulls, duplicates, and impossible numeric constraints).
* **`analysis.py`**: The automated Python script used to generate batch static visualizations.
* **`Group4_FinTech_Deck.md`**: The structured markdown content for the 13-slide executive pitch deck.

## 🚀 How to Run the Project Locally

### 1. View the Interactive Dashboard
To launch the Streamlit dashboard on your local machine:
```bash
# Install dependencies
pip install pandas streamlit plotly

# Run the dashboard
streamlit run dashboard.py
```

### 2. Run the Jupyter Notebook
To view the code and EDA step-by-step:
```bash
# Install Jupyter
pip install jupyter

# Launch notebook
jupyter notebook Group4_Analysis.ipynb
```

---
*This project was developed to showcase the bridge between raw data analysis and actionable product strategy.*
