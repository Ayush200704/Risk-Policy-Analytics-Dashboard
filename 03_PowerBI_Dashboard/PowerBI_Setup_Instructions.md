
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
