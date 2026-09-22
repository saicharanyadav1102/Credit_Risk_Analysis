import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration (Clean and Wide Layout)
st.set_page_config(page_title="PaySprint Dashboard", layout="wide")

# 2. Load the Cleaned Data
@st.cache_data
def load_data():
    # Load the cleaned dataset generated previously
    df = pd.read_csv("Group4_Cleaned.csv")
    return df

df = load_data()

# 3. Dashboard Header
st.title("💸 PaySprint Lending Dashboard")
st.markdown("**Focus:** Tracking rejection vs. default rates to identify underserved credit markets (e.g., Gig Workers).")

# 4. Sidebar Filters (Minimal & Necessary)
st.sidebar.header("Data Filters")
selected_employment = st.sidebar.multiselect(
    "Filter by Employment Type:",
    options=df['employment_type'].dropna().unique(),
    default=df['employment_type'].dropna().unique()
)

# Apply filter
filtered_df = df[df['employment_type'].isin(selected_employment)]

# Calculate KPIs
total_apps = len(filtered_df)
rejected_apps = len(filtered_df[filtered_df['application_status'] == 'Rejected'])
rejection_rate = (rejected_apps / total_apps * 100) if total_apps > 0 else 0

disbursed_df = filtered_df[filtered_df['disbursed_flag'] == 1]
defaults = disbursed_df['default_flag'].sum()
default_rate = (defaults / len(disbursed_df) * 100) if len(disbursed_df) > 0 else 0

# 5. Top KPI Cards
col1, col2, col3 = st.columns(3)
col1.metric("Total Applications", f"{total_apps:,}")
col2.metric("Avg. Rejection Rate", f"{rejection_rate:.1f}%")
col3.metric("Avg. Default Rate", f"{default_rate:.1f}%")

st.divider()

# 6. Core Visualizations (Side by Side)
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Rejection Rate by Employment")
    # Calculate rejection rate per employment type
    rej_df = filtered_df.groupby('employment_type').apply(
        lambda x: (x['application_status'] == 'Rejected').mean() * 100
    ).reset_index(name='Rejection Rate (%)')
    
    fig1 = px.bar(rej_df, x='employment_type', y='Rejection Rate (%)', 
                  color='employment_type', text_auto='.1f',
                  labels={'employment_type': 'Employment Type'})
    fig1.update_layout(showlegend=False)
    st.plotly_chart(fig1, use_container_width=True)

with col_right:
    st.subheader("Default Rate by Employment")
    # Calculate default rate per employment type
    def_df = disbursed_df.groupby('employment_type')['default_flag'].mean().reset_index()
    def_df['Default Rate (%)'] = def_df['default_flag'] * 100
    
    fig2 = px.bar(def_df, x='employment_type', y='Default Rate (%)', 
                  color='employment_type', text_auto='.1f',
                  labels={'employment_type': 'Employment Type'})
    fig2.update_layout(showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)

# 7. Bottom Section: Rejection Reasons
st.subheader("Why are loans being rejected?")
rej_reasons = filtered_df[filtered_df['application_status'] == 'Rejected']['rejection_reason'].value_counts().reset_index()
rej_reasons.columns = ['Reason', 'Count']

fig3 = px.pie(rej_reasons, names='Reason', values='Count', hole=0.4)
st.plotly_chart(fig3, use_container_width=True)
