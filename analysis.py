import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json

# Set plot style
sns.set_theme(style="whitegrid", font_scale=1.15)

# Load data
df = pd.read_csv(r"C:\Users\HP\OneDrive\Desktop\Growtech\group4_fintech_paysprint.csv")
report = {}
report['initial_shape'] = df.shape

# ----------------- PART A: DATA QUALITY -----------------

# 1. Duplicates
duplicates = df.duplicated().sum()
report['duplicates'] = int(duplicates)
df = df.drop_duplicates().reset_index(drop=True)
report['shape_after_dedup'] = df.shape

# 2. Clean text columns
text_cols = ['employment_type', 'product_type', 'kyc_status']
report['before_clean_value_counts'] = {col: df[col].value_counts().to_dict() for col in text_cols}

for col in text_cols:
    df[col] = df[col].astype(str).str.strip().str.title()

# Manual fixes for specific variants
df['product_type'] = df['product_type'].replace({
    'Bnpl': 'BNPL', 
    'Pl': 'Personal Loan'
})

df['kyc_status'] = df['kyc_status'].replace({
    'Nan': np.nan,
    'None': np.nan
})

report['after_clean_value_counts'] = {col: df[col].value_counts().to_dict() for col in text_cols}

# 3. Approved > Requested
invalid_approved = df[df['approved_amount_inr'] > df['requested_amount_inr']]
report['approved_gt_requested_count'] = len(invalid_approved)
# Fix: Cap approved amount at requested amount
df['approved_amount_inr'] = np.where(
    df['approved_amount_inr'] > df['requested_amount_inr'], 
    df['requested_amount_inr'], 
    df['approved_amount_inr']
)

# 4. Invalid Values
# Credit Score: 300 to 900
invalid_credit = df[(df['credit_score'] < 300) | (df['credit_score'] > 900)]
report['invalid_credit_score_count'] = len(invalid_credit)
df.loc[(df['credit_score'] < 300) | (df['credit_score'] > 900), 'credit_score'] = np.nan

# Customer Age: 18 to 80
invalid_age = df[(df['customer_age'] < 18) | (df['customer_age'] > 80)]
report['invalid_age_count'] = len(invalid_age)
df.loc[(df['customer_age'] < 18) | (df['customer_age'] > 80), 'customer_age'] = np.nan

# Monthly Income: < 0 is invalid
invalid_income = df[df['monthly_income_inr'] < 0]
report['invalid_income_count'] = len(invalid_income)
df.loc[df['monthly_income_inr'] < 0, 'monthly_income_inr'] = np.nan

# 5. Missing values
missing_counts = df[['approved_amount_inr', 'days_past_due', 'rejection_reason']].isnull().sum()
report['missing_counts_reasons'] = missing_counts.to_dict()

# 6. DTI Ratio
df['dti_ratio'] = df['existing_emi_inr'] / df['monthly_income_inr']
absurd_dti = df[(df['dti_ratio'] == np.inf) | (df['dti_ratio'] > 5)]
report['absurd_dti_count'] = len(absurd_dti)

# Save cleaned dataset
df.to_csv("Group4_Cleaned.csv", index=False)

# ----------------- PART B: EXPLORATION -----------------

# Save plots
# 1. Application status by product type
plt.figure(figsize=(10,6))
sns.countplot(data=df, x='product_type', hue='application_status')
plt.title("Application Status by Product Type")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("chart_app_status_product.png")

# 2. Rejection reason mix
plt.figure(figsize=(10,6))
rejected = df[df['application_status'] == 'Rejected']
sns.countplot(data=rejected, y='rejection_reason', order=rejected['rejection_reason'].value_counts().index)
plt.title("Rejection Reason Mix")
plt.tight_layout()
plt.savefig("chart_rejection_reasons.png")

# 3. Credit score distribution
plt.figure(figsize=(10,6))
sns.histplot(data=df[df['application_status'].isin(['Approved', 'Rejected'])], x='credit_score', hue='application_status', bins=30, kde=True)
plt.title("Credit Score Distribution by Approval")
plt.tight_layout()
plt.savefig("chart_credit_score_approval.png")

# 4. Defaults
df['dti_band'] = pd.cut(df['dti_ratio'], bins=[-1, 0.2, 0.4, 0.6, 1.0, 100], labels=['<20%', '20-40%', '40-60%', '60-100%', '>100%'])
default_rates = df[df['disbursed_flag'] == 1].groupby('dti_band')['default_flag'].mean()
plt.figure(figsize=(8,5))
default_rates.plot(kind='bar', color='#d84a6b')
plt.title("Default Rate by DTI Band")
plt.ylabel("Default Rate")
plt.tight_layout()
plt.savefig("chart_default_rate_dti.png")

# Correlation
corr = df.select_dtypes(include=[np.number]).corr()
plt.figure(figsize=(12,10))
sns.heatmap(corr, cmap="coolwarm", center=0)
plt.title("Correlation Heatmap")
plt.tight_layout()
plt.savefig("chart_correlation.png")

with open('report.json', 'w') as f:
    json.dump(report, f, indent=4)

print("Analysis complete.")
