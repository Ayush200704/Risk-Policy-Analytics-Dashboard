"""
Reserve Monitoring and Capital Adequacy Analysis
Author: Data Analyst
Date: April 2025
Purpose: Advanced reserve monitoring and capital adequacy scenario analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class ReserveMonitoring:
    def __init__(self, data_path):
        """Initialize reserve monitoring system"""
        self.data_path = data_path
        self.df = None
        self.reserve_analysis = None
        self.stress_test_results = None
        
    def load_and_prepare_data(self):
        """Load and prepare data for reserve analysis"""
        print("Loading data for reserve monitoring...")
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
        
        # Create risk categories
        df['Risk Score'] = self._calculate_risk_score(df)
        df['Risk Category'] = df['Risk Score'].apply(self._categorize_risk)
        
        # Calculate loss ratios
        df['Loss Ratio'] = (df['Previous Claims'] * 1000) / df['Premium Amount']
        df['Loss Ratio'] = df['Loss Ratio'].fillna(0)
        
        # Calculate policy duration
        current_date = datetime.now()
        df['Policy Duration Years'] = (current_date - df['Policy Start Date']).dt.days / 365.25
        
        self.df = df
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
    
    def calculate_reserve_requirements(self):
        """Calculate reserve requirements by risk category"""
        print("Calculating reserve requirements...")
        
        if self.df is None:
            self.load_and_prepare_data()
        
        df = self.df
        
        # Reserve calculation by risk category
        reserve_analysis = df.groupby('Risk Category').agg({
            'Premium Amount': ['sum', 'mean', 'count'],
            'Previous Claims': 'sum',
            'Loss Ratio': 'mean',
            'Policy Duration Years': 'mean'
        }).round(2)
        
        reserve_analysis.columns = ['Total Premiums', 'Avg Premium', 'Policy Count', 'Total Claims', 'Avg Loss Ratio', 'Avg Duration']
        reserve_analysis = reserve_analysis.reset_index()
        
        # Calculate reserve requirements using different methodologies
        
        # 1. Premium-based reserves (15% of annual premiums)
        reserve_analysis['Premium Based Reserves'] = reserve_analysis['Total Premiums'] * 0.15
        
        # 2. Claims-based reserves (3x average annual claims)
        reserve_analysis['Claims Based Reserves'] = (reserve_analysis['Total Claims'] * 1000) * 3
        
        # 3. Risk-adjusted reserves (varies by risk category)
        risk_multipliers = {'Low': 0.10, 'Medium': 0.15, 'High': 0.25, 'Very High': 0.35}
        reserve_analysis['Risk Adjusted Reserves'] = reserve_analysis.apply(
            lambda x: x['Total Premiums'] * risk_multipliers.get(x['Risk Category'], 0.15), axis=1
        )
        
        # 4. IBNR (Incurred But Not Reported) reserves
        reserve_analysis['IBNR Reserves'] = reserve_analysis['Total Premiums'] * 0.05
        
        # 5. Total required reserves (maximum of all methods)
        reserve_analysis['Total Required Reserves'] = reserve_analysis[
            ['Premium Based Reserves', 'Claims Based Reserves', 'Risk Adjusted Reserves', 'IBNR Reserves']
        ].max(axis=1)
        
        # Calculate actual claims exposure
        reserve_analysis['Actual Claims Exposure'] = reserve_analysis['Total Claims'] * 1000
        
        # Calculate reserve adequacy
        reserve_analysis['Reserve Adequacy'] = (
            reserve_analysis['Total Required Reserves'] - reserve_analysis['Actual Claims Exposure']
        )
        
        # Calculate reserve ratio
        reserve_analysis['Reserve Ratio'] = (
            reserve_analysis['Total Required Reserves'] / reserve_analysis['Actual Claims Exposure']
        )
        
        self.reserve_analysis = reserve_analysis
        return reserve_analysis
    
    def perform_stress_testing(self):
        """Perform comprehensive stress testing scenarios"""
        print("Performing stress testing scenarios...")
        
        if self.df is None:
            self.load_and_prepare_data()
        
        df = self.df
        
        # Base case metrics
        base_metrics = {
            'total_premiums': df['Premium Amount'].sum(),
            'total_claims': df['Previous Claims'].sum(),
            'total_policies': len(df),
            'avg_loss_ratio': df['Loss Ratio'].mean()
        }
        
        # Stress test scenarios
        scenarios = {
            'Base Case': {
                'claims_multiplier': 1.0,
                'premium_multiplier': 1.0,
                'description': 'Current baseline scenario'
            },
            'Mild Stress': {
                'claims_multiplier': 1.2,
                'premium_multiplier': 1.0,
                'description': '20% increase in claims frequency'
            },
            'Moderate Stress': {
                'claims_multiplier': 1.5,
                'premium_multiplier': 1.0,
                'description': '50% increase in claims frequency'
            },
            'Severe Stress': {
                'claims_multiplier': 2.0,
                'premium_multiplier': 1.0,
                'description': '100% increase in claims frequency'
            },
            'Economic Downturn': {
                'claims_multiplier': 1.8,
                'premium_multiplier': 0.9,
                'description': 'Economic downturn with reduced premiums'
            },
            'Catastrophic Event': {
                'claims_multiplier': 3.0,
                'premium_multiplier': 1.0,
                'description': 'Catastrophic event scenario'
            }
        }
        
        stress_results = []
        
        for scenario_name, params in scenarios.items():
            # Calculate stressed metrics
            stressed_claims = base_metrics['total_claims'] * params['claims_multiplier']
            stressed_premiums = base_metrics['total_premiums'] * params['premium_multiplier']
            stressed_loss_ratio = (stressed_claims * 1000) / stressed_premiums
            
            # Calculate required reserves under stress
            required_reserves = stressed_premiums * 0.15  # 15% of premiums as reserves
            actual_claims_exposure = stressed_claims * 1000
            
            # Calculate capital adequacy
            capital_adequacy = required_reserves - actual_claims_exposure
            capital_ratio = required_reserves / actual_claims_exposure if actual_claims_exposure > 0 else 0
            
            stress_results.append({
                'Scenario': scenario_name,
                'Description': params['description'],
                'Claims Multiplier': params['claims_multiplier'],
                'Premium Multiplier': params['premium_multiplier'],
                'Total Premiums': stressed_premiums,
                'Total Claims': stressed_claims,
                'Loss Ratio': stressed_loss_ratio,
                'Required Reserves': required_reserves,
                'Actual Claims Exposure': actual_claims_exposure,
                'Capital Adequacy': capital_adequacy,
                'Capital Ratio': capital_ratio,
                'Adequacy Status': 'Adequate' if capital_adequacy >= 0 else 'Inadequate'
            })
        
        self.stress_test_results = pd.DataFrame(stress_results)
        return self.stress_test_results
    
    def calculate_capital_adequacy_ratio(self):
        """Calculate capital adequacy ratios by risk category"""
        print("Calculating capital adequacy ratios...")
        
        if self.reserve_analysis is None:
            self.calculate_reserve_requirements()
        
        # Calculate overall capital adequacy
        total_required_reserves = self.reserve_analysis['Total Required Reserves'].sum()
        total_actual_exposure = self.reserve_analysis['Actual Claims Exposure'].sum()
        total_premiums = self.reserve_analysis['Total Premiums'].sum()
        
        # Capital adequacy ratios
        capital_ratios = {
            'Total Required Reserves': total_required_reserves,
            'Total Actual Exposure': total_actual_exposure,
            'Total Premiums': total_premiums,
            'Reserve Coverage Ratio': total_required_reserves / total_actual_exposure if total_actual_exposure > 0 else 0,
            'Premium Coverage Ratio': total_required_reserves / total_premiums if total_premiums > 0 else 0,
            'Overall Adequacy': total_required_reserves - total_actual_exposure
        }
        
        return capital_ratios
    
    def generate_reserve_monitoring_dashboard(self):
        """Generate comprehensive reserve monitoring dashboard"""
        print("Generating reserve monitoring dashboard...")
        
        if self.reserve_analysis is None:
            self.calculate_reserve_requirements()
        
        if self.stress_test_results is None:
            self.perform_stress_testing()
        
        # Create comprehensive dashboard
        fig, axes = plt.subplots(2, 3, figsize=(20, 12))
        fig.suptitle('Reserve Monitoring & Capital Adequacy Dashboard', fontsize=16, fontweight='bold')
        
        # 1. Reserve Requirements by Risk Category
        ax1 = axes[0, 0]
        categories = self.reserve_analysis['Risk Category']
        reserves = self.reserve_analysis['Total Required Reserves']
        bars = ax1.bar(categories, reserves, color=['green', 'yellow', 'orange', 'red'])
        ax1.set_title('Required Reserves by Risk Category')
        ax1.set_ylabel('Reserves ($)')
        ax1.tick_params(axis='x', rotation=45)
        
        # Add value labels on bars
        for bar, value in zip(bars, reserves):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(reserves)*0.01,
                    f'${value:,.0f}', ha='center', va='bottom', fontsize=8)
        
        # 2. Reserve Adequacy Status
        ax2 = axes[0, 1]
        adequacy = self.reserve_analysis['Reserve Adequacy']
        colors = ['green' if x >= 0 else 'red' for x in adequacy]
        bars = ax2.bar(categories, adequacy, color=colors)
        ax2.set_title('Reserve Adequacy by Risk Category')
        ax2.set_ylabel('Adequacy ($)')
        ax2.axhline(y=0, color='black', linestyle='--', alpha=0.5)
        ax2.tick_params(axis='x', rotation=45)
        
        # 3. Reserve Ratios
        ax3 = axes[0, 2]
        ratios = self.reserve_analysis['Reserve Ratio']
        bars = ax3.bar(categories, ratios, color='skyblue')
        ax3.set_title('Reserve Ratios by Risk Category')
        ax3.set_ylabel('Reserve Ratio')
        ax3.axhline(y=1, color='red', linestyle='--', alpha=0.5, label='Minimum Required')
        ax3.legend()
        ax3.tick_params(axis='x', rotation=45)
        
        # 4. Stress Test Results - Loss Ratios
        ax4 = axes[1, 0]
        scenarios = self.stress_test_results['Scenario']
        loss_ratios = self.stress_test_results['Loss Ratio']
        colors = ['green' if x < 0.7 else 'orange' if x < 1.0 else 'red' for x in loss_ratios]
        bars = ax4.bar(scenarios, loss_ratios, color=colors)
        ax4.set_title('Loss Ratios Under Stress Scenarios')
        ax4.set_ylabel('Loss Ratio')
        ax4.axhline(y=0.7, color='red', linestyle='--', alpha=0.5, label='Target Threshold')
        ax4.legend()
        ax4.tick_params(axis='x', rotation=45)
        
        # 5. Capital Adequacy Under Stress
        ax5 = axes[1, 1]
        adequacy_stress = self.stress_test_results['Capital Adequacy']
        colors = ['green' if x >= 0 else 'red' for x in adequacy_stress]
        bars = ax5.bar(scenarios, adequacy_stress, color=colors)
        ax5.set_title('Capital Adequacy Under Stress')
        ax5.set_ylabel('Capital Adequacy ($)')
        ax5.axhline(y=0, color='black', linestyle='--', alpha=0.5)
        ax5.tick_params(axis='x', rotation=45)
        
        # 6. Reserve Coverage Analysis
        ax6 = axes[1, 2]
        coverage_ratios = self.stress_test_results['Capital Ratio']
        bars = ax6.bar(scenarios, coverage_ratios, color='lightblue')
        ax6.set_title('Reserve Coverage Ratios')
        ax6.set_ylabel('Coverage Ratio')
        ax6.axhline(y=1, color='red', linestyle='--', alpha=0.5, label='Minimum Required')
        ax6.legend()
        ax6.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig('05_Data_Analysis/reserve_monitoring_dashboard.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return fig
    
    def generate_reserve_recommendations(self):
        """Generate reserve management recommendations"""
        print("Generating reserve management recommendations...")
        
        if self.reserve_analysis is None:
            self.calculate_reserve_requirements()
        
        recommendations = []
        
        # Analyze reserve adequacy by category
        for _, row in self.reserve_analysis.iterrows():
            category = row['Risk Category']
            adequacy = row['Reserve Adequacy']
            ratio = row['Reserve Ratio']
            
            if adequacy < 0:
                recommendations.append({
                    'Risk Category': category,
                    'Issue': 'Inadequate Reserves',
                    'Current Adequacy': f'${adequacy:,.2f}',
                    'Recommendation': f'Increase reserves by ${abs(adequacy):,.2f} to meet minimum requirements',
                    'Priority': 'High' if ratio < 0.5 else 'Medium'
                })
            elif ratio < 1.2:
                recommendations.append({
                    'Risk Category': category,
                    'Issue': 'Low Reserve Buffer',
                    'Current Adequacy': f'${adequacy:,.2f}',
                    'Recommendation': f'Consider increasing reserves by 20% to improve buffer',
                    'Priority': 'Medium'
                })
            else:
                recommendations.append({
                    'Risk Category': category,
                    'Issue': 'Adequate Reserves',
                    'Current Adequacy': f'${adequacy:,.2f}',
                    'Recommendation': 'Maintain current reserve levels',
                    'Priority': 'Low'
                })
        
        # Overall portfolio recommendations
        total_adequacy = self.reserve_analysis['Reserve Adequacy'].sum()
        if total_adequacy < 0:
            recommendations.append({
                'Risk Category': 'Overall Portfolio',
                'Issue': 'Portfolio-wide Reserve Shortfall',
                'Current Adequacy': f'${total_adequacy:,.2f}',
                'Recommendation': 'Implement immediate reserve increase across all categories',
                'Priority': 'Critical'
            })
        
        return pd.DataFrame(recommendations)
    
    def export_reserve_analysis(self, output_path='05_Data_Analysis/'):
        """Export reserve analysis results"""
        print(f"Exporting reserve analysis to {output_path}...")
        
        if self.reserve_analysis is None:
            self.calculate_reserve_requirements()
        
        if self.stress_test_results is None:
            self.perform_stress_testing()
        
        # Export reserve analysis
        self.reserve_analysis.to_csv(f'{output_path}reserve_analysis.csv', index=False)
        
        # Export stress test results
        self.stress_test_results.to_csv(f'{output_path}stress_test_results.csv', index=False)
        
        # Export recommendations
        recommendations = self.generate_reserve_recommendations()
        recommendations.to_csv(f'{output_path}reserve_recommendations.csv', index=False)
        
        # Export capital adequacy ratios
        capital_ratios = self.calculate_capital_adequacy_ratio()
        capital_df = pd.DataFrame(list(capital_ratios.items()), columns=['Metric', 'Value'])
        capital_df.to_csv(f'{output_path}capital_adequacy_ratios.csv', index=False)
        
        print("Reserve analysis export completed!")
        return True

def main():
    """Main execution function"""
    print("="*60)
    print("RESERVE MONITORING & CAPITAL ADEQUACY ANALYSIS")
    print("="*60)
    
    # Initialize reserve monitoring
    reserve_monitor = ReserveMonitoring('Insurance Premium Prediction Dataset.csv')
    
    # Load and prepare data
    reserve_monitor.load_and_prepare_data()
    
    # Calculate reserve requirements
    reserve_analysis = reserve_monitor.calculate_reserve_requirements()
    
    # Perform stress testing
    stress_results = reserve_monitor.perform_stress_testing()
    
    # Calculate capital adequacy
    capital_ratios = reserve_monitor.calculate_capital_adequacy_ratio()
    
    # Generate dashboard
    reserve_monitor.generate_reserve_monitoring_dashboard()
    
    # Generate recommendations
    recommendations = reserve_monitor.generate_reserve_recommendations()
    
    # Export results
    reserve_monitor.export_reserve_analysis()
    
    print("\n" + "="*60)
    print("RESERVE MONITORING ANALYSIS COMPLETED!")
    print("="*60)
    
    return reserve_monitor

if __name__ == "__main__":
    reserve_monitor = main()
