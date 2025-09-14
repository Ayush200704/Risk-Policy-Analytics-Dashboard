"""
Power BI Data Preparation Script
Author: Data Analyst
Date: April 2025
Purpose: Prepare and export data specifically for Power BI dashboard
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class PowerBIDataPrep:
    def __init__(self, data_path):
        """Initialize Power BI data preparation"""
        self.data_path = data_path
        self.df = None
        self.powerbi_data = None
        
    def load_and_prepare_data(self):
        """Load and prepare data specifically for Power BI"""
        print("Loading data for Power BI preparation...")
        self.df = pd.read_csv(self.data_path)
        
        # Clean and prepare data
        df = self.df.copy()
        
        # Handle missing values
        df['Age'] = df['Age'].fillna(df['Age'].median())
        df['Annual Income'] = df['Annual Income'].fillna(df['Annual Income'].median())
        df['Number of Dependents'] = df['Number of Dependents'].fillna(0)
        df['Health Score'] = df['Health Score'].fillna(df['Health Score'].median())
        df['Previous Claims'] = df['Previous Claims'].fillna(0)
        df['Credit Score'] = df['Credit Score'].fillna(df['Credit Score'].median())
        df['Customer Feedback'] = df['Customer Feedback'].fillna('Average')
        
        # Convert dates
        df['Policy Start Date'] = pd.to_datetime(df['Policy Start Date'])
        
        # Create calculated columns for Power BI
        df['Age Group'] = pd.cut(df['Age'], bins=[0, 25, 35, 45, 55, 65, 100], 
                                labels=['18-25', '26-35', '36-45', '46-55', '56-65', '65+'])
        
        df['Income Group'] = pd.cut(df['Annual Income'], bins=[0, 30000, 60000, 100000, 200000, float('inf')], 
                                   labels=['Low', 'Lower-Mid', 'Mid', 'Upper-Mid', 'High'])
        
        # Risk calculation
        df['Risk Score'] = self._calculate_risk_score(df)
        df['Risk Category'] = df['Risk Score'].apply(self._categorize_risk)
        
        # Premium metrics
        df['Premium Per Year'] = df['Premium Amount'] / df['Insurance Duration']
        df['Loss Ratio'] = (df['Previous Claims'] * 1000) / df['Premium Amount']
        df['Loss Ratio'] = df['Loss Ratio'].fillna(0)
        
        # Customer value
        df['Customer Value'] = df['Premium Amount'] * df['Insurance Duration']
        
        # Policy duration in years
        current_date = datetime.now()
        df['Policy Duration Years'] = (current_date - df['Policy Start Date']).dt.days / 365.25
        
        # Create time-based columns for Power BI
        df['Year'] = df['Policy Start Date'].dt.year
        df['Month'] = df['Policy Start Date'].dt.month
        df['Quarter'] = df['Policy Start Date'].dt.quarter
        
        self.powerbi_data = df
        return df
    
    def _calculate_risk_score(self, df):
        """Calculate risk score for each policy"""
        risk_scores = []
        
        for _, row in df.iterrows():
            score = 0
            
            # Age factor
            if row['Age'] < 25 or row['Age'] > 65:
                score += 2
            elif 25 <= row['Age'] <= 35:
                score += 1
            
            # Claims history
            if row['Previous Claims'] > 2:
                score += 3
            elif row['Previous Claims'] > 0:
                score += 1
            
            # Health score
            if row['Health Score'] < 20:
                score += 2
            elif row['Health Score'] < 40:
                score += 1
            
            # Credit score
            if row['Credit Score'] < 500:
                score += 2
            elif row['Credit Score'] < 650:
                score += 1
            
            # Smoking status
            if row['Smoking Status'] == 'Yes':
                score += 2
            
            # Exercise frequency
            if row['Exercise Frequency'] == 'Rarely':
                score += 1
            
            risk_scores.append(score)
        
        return risk_scores
    
    def _categorize_risk(self, score):
        """Categorize risk based on score"""
        if score <= 2:
            return 'Low'
        elif score <= 4:
            return 'Medium'
        elif score <= 6:
            return 'High'
        else:
            return 'Very High'
    
    def create_summary_tables(self):
        """Create summary tables for Power BI"""
        if self.powerbi_data is None:
            self.load_and_prepare_data()
        
        df = self.powerbi_data
        
        # 1. Policy Performance Summary
        policy_summary = df.groupby(['Policy Type', 'Risk Category']).agg({
            'Premium Amount': ['count', 'sum', 'mean', 'median'],
            'Previous Claims': ['sum', 'mean'],
            'Loss Ratio': 'mean',
            'Customer Value': 'sum'
        }).round(2)
        
        policy_summary.columns = ['Policy Count', 'Total Premiums', 'Avg Premium', 'Median Premium',
                                 'Total Claims', 'Avg Claims', 'Avg Loss Ratio', 'Total Customer Value']
        policy_summary = policy_summary.reset_index()
        
        # 2. Monthly Trends
        monthly_trends = df.groupby(['Year', 'Month']).agg({
            'Premium Amount': ['count', 'sum', 'mean'],
            'Previous Claims': 'sum',
            'Loss Ratio': 'mean'
        }).round(2)
        
        monthly_trends.columns = ['New Policies', 'Monthly Premiums', 'Avg Premium', 'Monthly Claims', 'Avg Loss Ratio']
        monthly_trends = monthly_trends.reset_index()
        
        # 3. Demographics Analysis
        demographics = df.groupby(['Age Group', 'Gender', 'Location']).agg({
            'Premium Amount': ['count', 'sum', 'mean'],
            'Previous Claims': 'mean',
            'Loss Ratio': 'mean',
            'Risk Score': 'mean'
        }).round(2)
        
        demographics.columns = ['Policy Count', 'Total Premiums', 'Avg Premium', 'Avg Claims', 'Avg Loss Ratio', 'Avg Risk Score']
        demographics = demographics.reset_index()
        
        # 4. Customer Segmentation
        customer_segments = df.groupby(['Income Group', 'Risk Category']).agg({
            'Premium Amount': ['count', 'sum', 'mean'],
            'Customer Value': 'mean',
            'Previous Claims': 'mean',
            'Loss Ratio': 'mean'
        }).round(2)
        
        customer_segments.columns = ['Customer Count', 'Total Premiums', 'Avg Premium', 'Avg Customer Value', 'Avg Claims', 'Avg Loss Ratio']
        customer_segments = customer_segments.reset_index()
        
        # 5. Location Performance
        location_performance = df.groupby('Location').agg({
            'Premium Amount': ['count', 'sum', 'mean'],
            'Previous Claims': ['sum', 'mean'],
            'Loss Ratio': 'mean',
            'Risk Score': 'mean'
        }).round(2)
        
        location_performance.columns = ['Policy Count', 'Total Premiums', 'Avg Premium', 'Total Claims', 'Avg Claims', 'Avg Loss Ratio', 'Avg Risk Score']
        location_performance = location_performance.reset_index()
        
        return {
            'policy_summary': policy_summary,
            'monthly_trends': monthly_trends,
            'demographics': demographics,
            'customer_segments': customer_segments,
            'location_performance': location_performance
        }
    
    def create_kpi_metrics(self):
        """Create KPI metrics for Power BI"""
        if self.powerbi_data is None:
            self.load_and_prepare_data()
        
        df = self.powerbi_data
        
        # Calculate key metrics
        total_policies = len(df)
        total_premiums = df['Premium Amount'].sum()
        avg_premium = df['Premium Amount'].mean()
        total_claims = df['Previous Claims'].sum()
        overall_loss_ratio = (df['Previous Claims'] * 1000).sum() / df['Premium Amount'].sum()
        
        # Risk distribution
        risk_distribution = df['Risk Category'].value_counts()
        
        # High-risk policies
        high_risk_policies = len(df[df['Risk Category'].isin(['High', 'Very High'])])
        high_risk_pct = (high_risk_policies / total_policies) * 100
        
        # Customer satisfaction
        satisfaction_data = df[df['Customer Feedback'].notna()]
        if len(satisfaction_data) > 0:
            good_satisfaction = len(satisfaction_data[satisfaction_data['Customer Feedback'].isin(['Good', 'Excellent'])])
            satisfaction_rate = (good_satisfaction / len(satisfaction_data)) * 100
        else:
            satisfaction_rate = 0
        
        # Create KPI dataframe
        kpi_data = pd.DataFrame({
            'Metric': [
                'Total Policies',
                'Total Premium Volume',
                'Average Premium',
                'Total Claims',
                'Overall Loss Ratio',
                'High Risk Policies (%)',
                'Customer Satisfaction (%)',
                'Average Risk Score',
                'Average Age',
                'Average Health Score'
            ],
            'Value': [
                total_policies,
                total_premiums,
                avg_premium,
                total_claims,
                overall_loss_ratio,
                high_risk_pct,
                satisfaction_rate,
                df['Risk Score'].mean(),
                df['Age'].mean(),
                df['Health Score'].mean()
            ]
        })
        
        return kpi_data, risk_distribution
    
    def export_for_powerbi(self, output_path='03_PowerBI_Dashboard/'):
        """Export all data for Power BI"""
        print(f"Exporting data for Power BI to {output_path}...")
        
        if self.powerbi_data is None:
            self.load_and_prepare_data()
        
        # Export main dataset
        self.powerbi_data.to_csv(f'{output_path}insurance_data_powerbi.csv', index=False)
        
        # Create and export summary tables
        summary_tables = self.create_summary_tables()
        
        for table_name, table_data in summary_tables.items():
            table_data.to_csv(f'{output_path}{table_name}.csv', index=False)
        
        # Export KPI metrics
        kpi_data, risk_dist = self.create_kpi_metrics()
        kpi_data.to_csv(f'{output_path}kpi_metrics.csv', index=False)
        risk_dist.to_csv(f'{output_path}risk_distribution.csv', index=False)
        
        # Create Power BI connection file
        self._create_powerbi_connection_file(output_path)
        
        print("Power BI data export completed!")
        return summary_tables, kpi_data
    
    def _create_powerbi_connection_file(self, output_path):
        """Create Power BI connection instructions"""
        connection_instructions = """
# Power BI Dashboard Setup Instructions

## Data Sources
1. Main Dataset: insurance_data_powerbi.csv
2. Summary Tables: policy_summary.csv, monthly_trends.csv, demographics.csv, customer_segments.csv, location_performance.csv
3. KPI Metrics: kpi_metrics.csv, risk_distribution.csv

## Recommended Visualizations

### 1. Executive Dashboard
- KPI Cards: Total Policies, Total Premium Volume, Average Premium, Loss Ratio
- Risk Distribution Pie Chart
- Customer Satisfaction Gauge

### 2. Policy Performance Analysis
- Premium by Policy Type (Bar Chart)
- Loss Ratio by Risk Category (Column Chart)
- Premium Trends Over Time (Line Chart)

### 3. Risk Analysis
- Risk Category Distribution
- High-Risk Policy Identification Table
- Risk Score vs Premium Scatter Plot

### 4. Customer Segmentation
- Customer Value by Income Group
- Demographics Analysis (Age, Gender, Location)
- Customer Feedback Analysis

### 5. Geographic Analysis
- Premium Performance by Location (Map)
- Loss Ratio by Location (Bar Chart)

### 6. Reserve Monitoring
- Reserve Adequacy by Risk Category
- Capital Adequacy Scenarios
- Stress Testing Results

## Calculated Measures (DAX)
```
Total Premium Volume = SUM(insurance_data_powerbi[Premium Amount])
Average Premium = AVERAGE(insurance_data_powerbi[Premium Amount])
Loss Ratio = DIVIDE(SUM(insurance_data_powerbi[Previous Claims]) * 1000, SUM(insurance_data_powerbi[Premium Amount]))
High Risk Count = CALCULATE(COUNT(insurance_data_powerbi[Policy ID]), insurance_data_powerbi[Risk Category] IN ("High", "Very High"))
```

## Filters
- Date Range (Policy Start Date)
- Policy Type
- Risk Category
- Location
- Age Group
- Income Group

## Refresh Settings
- Set up automatic refresh to update data daily
- Configure data source credentials
- Schedule refresh during off-peak hours
"""
        
        with open(f'{output_path}PowerBI_Setup_Instructions.md', 'w') as f:
            f.write(connection_instructions)

def main():
    """Main execution function"""
    print("="*60)
    print("POWER BI DATA PREPARATION")
    print("="*60)
    
    # Initialize Power BI data preparation
    powerbi_prep = PowerBIDataPrep('Insurance Premium Prediction Dataset.csv')
    
    # Load and prepare data
    powerbi_data = powerbi_prep.load_and_prepare_data()
    
    # Create summary tables
    summary_tables = powerbi_prep.create_summary_tables()
    
    # Create KPI metrics
    kpi_data, risk_dist = powerbi_prep.create_kpi_metrics()
    
    # Export for Power BI
    powerbi_prep.export_for_powerbi()
    
    print("\n" + "="*60)
    print("POWER BI DATA PREPARATION COMPLETED!")
    print("="*60)
    
    return powerbi_prep

if __name__ == "__main__":
    powerbi_prep = main()
