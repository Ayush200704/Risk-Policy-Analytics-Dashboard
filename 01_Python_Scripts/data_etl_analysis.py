"""
Risk & Policy Analytics Dashboard - ETL and Analysis Script
Author: Data Analyst
Date: April 2025
Purpose: Comprehensive data processing, analysis, and modeling for insurance policy performance
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Set up plotting style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class InsuranceAnalytics:
    def __init__(self, data_path):
        """Initialize the analytics class with data loading and preprocessing"""
        self.data_path = data_path
        self.df = None
        self.processed_df = None
        self.load_data()
        
    def load_data(self):
        """Load and perform initial data exploration"""
        print("Loading insurance dataset...")
        self.df = pd.read_csv(self.data_path)
        print(f"Dataset loaded: {self.df.shape[0]} records, {self.df.shape[1]} columns")
        
    def data_preprocessing(self):
        """Comprehensive data preprocessing and cleaning"""
        print("\nStarting data preprocessing...")
        df = self.df.copy()
        
        # Handle missing values
        print("Handling missing values...")
        
        # Age: Fill with median by gender and marital status
        df['Age'] = df.groupby(['Gender', 'Marital Status'])['Age'].transform(
            lambda x: x.fillna(x.median())
        )
        
        # Annual Income: Fill with median by occupation and education
        df['Annual Income'] = df.groupby(['Occupation', 'Education Level'])['Annual Income'].transform(
            lambda x: x.fillna(x.median())
        )
        
        # Number of Dependents: Fill with mode by marital status
        df['Number of Dependents'] = df.groupby('Marital Status')['Number of Dependents'].transform(
            lambda x: x.fillna(x.mode()[0] if not x.mode().empty else 0)
        )
        
        # Health Score: Fill with median by age group and smoking status
        df['Health Score'] = df.groupby(['Smoking Status', pd.cut(df['Age'], bins=5)])['Health Score'].transform(
            lambda x: x.fillna(x.median())
        )
        
        # Previous Claims: Fill with 0 for missing values
        df['Previous Claims'] = df['Previous Claims'].fillna(0)
        
        # Credit Score: Fill with median by income group
        df['Credit Score'] = df.groupby(pd.cut(df['Annual Income'], bins=5))['Credit Score'].transform(
            lambda x: x.fillna(x.median())
        )
        
        # Customer Feedback: Fill with 'Average' for missing values
        df['Customer Feedback'] = df['Customer Feedback'].fillna('Average')
        
        # Convert Policy Start Date to datetime
        df['Policy Start Date'] = pd.to_datetime(df['Policy Start Date'])
        
        # Create derived features
        print("Creating derived features...")
        
        # Age groups
        df['Age Group'] = pd.cut(df['Age'], bins=[0, 25, 35, 45, 55, 65, 100], 
                                labels=['18-25', '26-35', '36-45', '46-55', '56-65', '65+'])
        
        # Income groups
        df['Income Group'] = pd.cut(df['Annual Income'], bins=[0, 30000, 60000, 100000, 200000, float('inf')], 
                                   labels=['Low', 'Lower-Mid', 'Mid', 'Upper-Mid', 'High'])
        
        # Risk categories based on multiple factors
        df['Risk Category'] = self._calculate_risk_category(df)
        
        # Policy duration in years
        current_date = datetime.now()
        df['Policy Duration Years'] = (current_date - df['Policy Start Date']).dt.days / 365.25
        
        # Premium per year
        df['Premium Per Year'] = df['Premium Amount'] / df['Insurance Duration']
        
        # Loss ratio estimation (simplified)
        df['Estimated Loss Ratio'] = (df['Previous Claims'] * 1000) / df['Premium Amount']
        df['Estimated Loss Ratio'] = df['Estimated Loss Ratio'].fillna(0)
        
        self.processed_df = df
        print("Data preprocessing completed!")
        return df
    
    def _calculate_risk_category(self, df):
        """Calculate risk category based on multiple factors"""
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
            
            # Determine risk category
            if score <= 2:
                risk_scores.append('Low')
            elif score <= 4:
                risk_scores.append('Medium')
            elif score <= 6:
                risk_scores.append('High')
            else:
                risk_scores.append('Very High')
        
        return risk_scores
    
    def generate_summary_statistics(self):
        """Generate comprehensive summary statistics"""
        print("\nGenerating summary statistics...")
        
        if self.processed_df is None:
            self.data_preprocessing()
        
        df = self.processed_df
        
        # Basic statistics
        summary = {
            'Total Policies': len(df),
            'Total Premium Volume': df['Premium Amount'].sum(),
            'Average Premium': df['Premium Amount'].mean(),
            'Median Premium': df['Premium Amount'].median(),
            'Average Age': df['Age'].mean(),
            'Average Health Score': df['Health Score'].mean(),
            'Average Credit Score': df['Credit Score'].mean(),
            'Total Claims': df['Previous Claims'].sum(),
            'Average Loss Ratio': df['Estimated Loss Ratio'].mean()
        }
        
        # Policy type distribution
        policy_dist = df['Policy Type'].value_counts()
        
        # Risk category distribution
        risk_dist = df['Risk Category'].value_counts()
        
        # Location distribution
        location_dist = df['Location'].value_counts()
        
        return summary, policy_dist, risk_dist, location_dist
    
    def analyze_premium_trends(self):
        """Analyze premium trends and patterns"""
        print("\nAnalyzing premium trends...")
        
        if self.processed_df is None:
            self.data_preprocessing()
        
        df = self.processed_df
        
        # Premium analysis by various factors
        premium_analysis = {}
        
        # By policy type
        premium_analysis['by_policy_type'] = df.groupby('Policy Type')['Premium Amount'].agg(['mean', 'median', 'std', 'count'])
        
        # By risk category
        premium_analysis['by_risk_category'] = df.groupby('Risk Category')['Premium Amount'].agg(['mean', 'median', 'std', 'count'])
        
        # By age group
        premium_analysis['by_age_group'] = df.groupby('Age Group')['Premium Amount'].agg(['mean', 'median', 'std', 'count'])
        
        # By location
        premium_analysis['by_location'] = df.groupby('Location')['Premium Amount'].agg(['mean', 'median', 'std', 'count'])
        
        # By income group
        premium_analysis['by_income_group'] = df.groupby('Income Group')['Premium Amount'].agg(['mean', 'median', 'std', 'count'])
        
        return premium_analysis
    
    def calculate_loss_ratios(self):
        """Calculate and analyze loss ratios"""
        print("\nCalculating loss ratios...")
        
        if self.processed_df is None:
            self.data_preprocessing()
        
        df = self.processed_df
        
        # Overall loss ratio
        total_premiums = df['Premium Amount'].sum()
        total_claims = (df['Previous Claims'] * 1000).sum()  # Assuming average claim is $1000
        overall_loss_ratio = total_claims / total_premiums if total_premiums > 0 else 0
        
        # Loss ratios by category
        loss_ratios = {}
        
        for category in ['Policy Type', 'Risk Category', 'Location', 'Age Group']:
            category_loss_ratios = df.groupby(category).apply(
                lambda x: (x['Previous Claims'] * 1000).sum() / x['Premium Amount'].sum() 
                if x['Premium Amount'].sum() > 0 else 0
            )
            loss_ratios[category] = category_loss_ratios
        
        return overall_loss_ratio, loss_ratios
    
    def generate_visualizations(self, save_path='05_Data_Analysis/'):
        """Generate comprehensive visualizations"""
        print(f"\nGenerating visualizations in {save_path}...")
        
        if self.processed_df is None:
            self.data_preprocessing()
        
        df = self.processed_df
        
        # Set up the plotting environment
        plt.rcParams['figure.figsize'] = (12, 8)
        
        # 1. Premium Distribution
        plt.figure(figsize=(15, 10))
        
        plt.subplot(2, 3, 1)
        plt.hist(df['Premium Amount'], bins=50, alpha=0.7, edgecolor='black')
        plt.title('Premium Amount Distribution')
        plt.xlabel('Premium Amount ($)')
        plt.ylabel('Frequency')
        
        # 2. Premium by Policy Type
        plt.subplot(2, 3, 2)
        df.boxplot(column='Premium Amount', by='Policy Type', ax=plt.gca())
        plt.title('Premium by Policy Type')
        plt.suptitle('')  # Remove default title
        
        # 3. Risk Category Distribution
        plt.subplot(2, 3, 3)
        risk_counts = df['Risk Category'].value_counts()
        plt.pie(risk_counts.values, labels=risk_counts.index, autopct='%1.1f%%')
        plt.title('Risk Category Distribution')
        
        # 4. Premium vs Age
        plt.subplot(2, 3, 4)
        plt.scatter(df['Age'], df['Premium Amount'], alpha=0.5)
        plt.title('Premium vs Age')
        plt.xlabel('Age')
        plt.ylabel('Premium Amount ($)')
        
        # 5. Loss Ratio by Risk Category
        plt.subplot(2, 3, 5)
        loss_ratios = df.groupby('Risk Category')['Estimated Loss Ratio'].mean()
        loss_ratios.plot(kind='bar')
        plt.title('Average Loss Ratio by Risk Category')
        plt.ylabel('Loss Ratio')
        plt.xticks(rotation=45)
        
        # 6. Premium Trends by Location
        plt.subplot(2, 3, 6)
        location_premiums = df.groupby('Location')['Premium Amount'].mean()
        location_premiums.plot(kind='bar')
        plt.title('Average Premium by Location')
        plt.ylabel('Average Premium ($)')
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        plt.savefig(f'{save_path}comprehensive_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        # Additional detailed visualizations
        self._create_detailed_visualizations(df, save_path)
    
    def _create_detailed_visualizations(self, df, save_path):
        """Create additional detailed visualizations"""
        
        # Correlation heatmap
        plt.figure(figsize=(12, 8))
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        correlation_matrix = df[numeric_cols].corr()
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
        plt.title('Correlation Matrix of Numeric Variables')
        plt.tight_layout()
        plt.savefig(f'{save_path}correlation_heatmap.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        # Premium analysis by multiple factors
        plt.figure(figsize=(15, 10))
        
        # Premium by Age Group and Policy Type
        plt.subplot(2, 2, 1)
        premium_pivot = df.pivot_table(values='Premium Amount', index='Age Group', 
                                     columns='Policy Type', aggfunc='mean')
        sns.heatmap(premium_pivot, annot=True, fmt='.0f', cmap='YlOrRd')
        plt.title('Average Premium by Age Group and Policy Type')
        
        # Claims vs Premium scatter
        plt.subplot(2, 2, 2)
        plt.scatter(df['Previous Claims'], df['Premium Amount'], alpha=0.5)
        plt.title('Previous Claims vs Premium Amount')
        plt.xlabel('Previous Claims')
        plt.ylabel('Premium Amount ($)')
        
        # Health Score vs Premium
        plt.subplot(2, 2, 3)
        plt.scatter(df['Health Score'], df['Premium Amount'], alpha=0.5)
        plt.title('Health Score vs Premium Amount')
        plt.xlabel('Health Score')
        plt.ylabel('Premium Amount ($)')
        
        # Credit Score vs Premium
        plt.subplot(2, 2, 4)
        plt.scatter(df['Credit Score'], df['Premium Amount'], alpha=0.5)
        plt.title('Credit Score vs Premium Amount')
        plt.xlabel('Credit Score')
        plt.ylabel('Premium Amount ($)')
        
        plt.tight_layout()
        plt.savefig(f'{save_path}detailed_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def export_processed_data(self, output_path='05_Data_Analysis/'):
        """Export processed data for further analysis"""
        print(f"\nExporting processed data to {output_path}...")
        
        if self.processed_df is None:
            self.data_preprocessing()
        
        # Export main processed dataset
        self.processed_df.to_csv(f'{output_path}processed_insurance_data.csv', index=False)
        
        # Export summary statistics
        summary, policy_dist, risk_dist, location_dist = self.generate_summary_statistics()
        
        summary_df = pd.DataFrame(list(summary.items()), columns=['Metric', 'Value'])
        summary_df.to_csv(f'{output_path}summary_statistics.csv', index=False)
        
        # Export premium analysis
        premium_analysis = self.analyze_premium_trends()
        
        # Export loss ratio analysis
        overall_loss_ratio, loss_ratios = self.calculate_loss_ratios()
        
        loss_ratio_summary = {
            'Overall Loss Ratio': overall_loss_ratio,
            'Loss Ratios by Category': loss_ratios
        }
        
        print("Data export completed!")
        return summary_df, premium_analysis, loss_ratio_summary

def main():
    """Main execution function"""
    print("="*60)
    print("RISK & POLICY ANALYTICS DASHBOARD - ETL PROCESS")
    print("="*60)
    
    # Initialize analytics
    analytics = InsuranceAnalytics('Insurance Premium Prediction Dataset.csv')
    
    # Perform data preprocessing
    processed_data = analytics.data_preprocessing()
    
    # Generate analysis
    summary_stats = analytics.generate_summary_statistics()
    premium_analysis = analytics.analyze_premium_trends()
    loss_ratios = analytics.calculate_loss_ratios()
    
    # Create visualizations
    analytics.generate_visualizations()
    
    # Export data
    analytics.export_processed_data()
    
    print("\n" + "="*60)
    print("ETL PROCESS COMPLETED SUCCESSFULLY!")
    print("="*60)
    
    return analytics

if __name__ == "__main__":
    analytics = main()
