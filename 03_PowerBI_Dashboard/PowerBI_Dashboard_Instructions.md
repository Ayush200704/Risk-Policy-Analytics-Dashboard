# Power BI Dashboard Setup Instructions

## Overview
This document provides step-by-step instructions for setting up the Risk & Policy Analytics Dashboard in Microsoft Power BI Desktop.

## Data Sources

### Primary Dataset
- **File**: `insurance_data_powerbi.csv`
- **Location**: `03_PowerBI_Dashboard/`
- **Records**: 278,860 insurance policies
- **Fields**: 20+ columns including demographics, financial, and policy data

### Supporting Tables
- `policy_summary.csv` - Policy performance summary by type and risk category
- `monthly_trends.csv` - Time-series trend data
- `demographics.csv` - Demographics analysis
- `customer_segments.csv` - Customer segmentation data
- `location_performance.csv` - Geographic performance metrics
- `kpi_metrics.csv` - Key performance indicators
- `risk_distribution.csv` - Risk category distribution

## Dashboard Pages

### 1. Executive Dashboard
**Purpose**: High-level overview for executives and stakeholders

**Visualizations**:
- **KPI Cards**: Total Policies, Total Premium Volume, Average Premium, Loss Ratio
- **Risk Distribution**: Pie chart showing risk category distribution
- **Customer Satisfaction**: Gauge showing satisfaction percentage
- **Premium Trends**: Line chart showing premium trends over time
- **Top Performing Policies**: Table showing best performing policy types

**Filters**:
- Date Range (Policy Start Date)
- Policy Type
- Risk Category
- Location

### 2. Policy Performance Analysis
**Purpose**: Detailed analysis of policy performance metrics

**Visualizations**:
- **Premium by Policy Type**: Bar chart comparing premiums across policy types
- **Loss Ratio Analysis**: Column chart showing loss ratios by risk category
- **Premium Distribution**: Histogram showing premium amount distribution
- **Claims Frequency**: Scatter plot showing claims vs premiums
- **Performance Matrix**: Heatmap showing performance by age group and policy type

**Key Metrics**:
- Average Premium by Policy Type
- Loss Ratio by Risk Category
- Claims Frequency
- Customer Retention Rate

### 3. Risk Analysis
**Purpose**: Comprehensive risk assessment and monitoring

**Visualizations**:
- **Risk Category Distribution**: Donut chart showing risk distribution
- **High-Risk Policy Table**: Table identifying high-risk policies
- **Risk Score Distribution**: Histogram showing risk score distribution
- **Risk vs Premium Scatter**: Scatter plot showing risk score vs premium
- **Risk Trends**: Line chart showing risk trends over time

**Alerts**:
- High-risk policy count threshold
- Risk score trend alerts
- Premium adequacy warnings

### 4. Customer Segmentation
**Purpose**: Customer analysis and segmentation insights

**Visualizations**:
- **Customer Value by Income Group**: Bar chart showing value by income
- **Demographics Analysis**: Multiple charts for age, gender, location
- **Customer Feedback Analysis**: Stacked bar chart showing feedback distribution
- **Customer Lifetime Value**: Scatter plot showing value vs duration
- **Segmentation Matrix**: Cross-tabulation of key customer attributes

**Segments**:
- High Value Customers
- Medium Value Customers
- Low Value Customers
- At-Risk Customers

### 5. Geographic Analysis
**Purpose**: Location-based performance analysis

**Visualizations**:
- **Premium Performance by Location**: Map visualization (if available)
- **Loss Ratio by Location**: Bar chart comparing loss ratios
- **Location Performance Matrix**: Table showing key metrics by location
- **Geographic Risk Distribution**: Heatmap showing risk by location
- **Location Trends**: Line chart showing performance trends by location

### 6. Reserve Monitoring
**Purpose**: Reserve adequacy and capital management

**Visualizations**:
- **Reserve Adequacy by Risk Category**: Bar chart showing reserve levels
- **Capital Adequacy Scenarios**: Line chart showing stress test results
- **Reserve Coverage Ratios**: Gauge showing coverage adequacy
- **Reserve Trends**: Line chart showing reserve trends over time
- **Stress Test Results**: Table showing stress test outcomes

## Calculated Measures (DAX)

### Key Performance Indicators
```dax
Total Premium Volume = SUM(insurance_data_powerbi[Premium Amount])

Average Premium = AVERAGE(insurance_data_powerbi[Premium Amount])

Overall Loss Ratio = 
DIVIDE(
    SUM(insurance_data_powerbi[Previous Claims]) * 1000,
    SUM(insurance_data_powerbi[Premium Amount])
)

High Risk Count = 
CALCULATE(
    COUNT(insurance_data_powerbi[Policy ID]),
    insurance_data_powerbi[Risk Category] IN ("High", "Very High")
)

High Risk Percentage = 
DIVIDE(
    [High Risk Count],
    COUNT(insurance_data_powerbi[Policy ID])
)

Customer Satisfaction Rate = 
DIVIDE(
    COUNTROWS(
        FILTER(
            insurance_data_powerbi,
            insurance_data_powerbi[Customer Feedback] IN ("Good", "Excellent")
        )
    ),
    COUNTROWS(
        FILTER(
            insurance_data_powerbi,
            NOT(ISBLANK(insurance_data_powerbi[Customer Feedback]))
        )
    )
)
```

### Risk Analysis Measures
```dax
Average Risk Score = AVERAGE(insurance_data_powerbi[Risk Score])

Risk Category Count = 
SWITCH(
    SELECTEDVALUE(insurance_data_powerbi[Risk Category]),
    "Low", COUNTROWS(FILTER(insurance_data_powerbi, insurance_data_powerbi[Risk Category] = "Low")),
    "Medium", COUNTROWS(FILTER(insurance_data_powerbi, insurance_data_powerbi[Risk Category] = "Medium")),
    "High", COUNTROWS(FILTER(insurance_data_powerbi, insurance_data_powerbi[Risk Category] = "High")),
    "Very High", COUNTROWS(FILTER(insurance_data_powerbi, insurance_data_powerbi[Risk Category] = "Very High"))
)

Premium per Risk Category = 
DIVIDE(
    SUM(insurance_data_powerbi[Premium Amount]),
    [Risk Category Count]
)
```

### Reserve Monitoring Measures
```dax
Required Reserves = SUM(insurance_data_powerbi[Premium Amount]) * 0.15

Actual Claims Exposure = SUM(insurance_data_powerbi[Previous Claims]) * 1000

Reserve Adequacy = [Required Reserves] - [Actual Claims Exposure]

Reserve Coverage Ratio = 
DIVIDE(
    [Required Reserves],
    [Actual Claims Exposure]
)

Capital Adequacy Status = 
IF(
    [Reserve Adequacy] >= 0,
    "Adequate",
    "Inadequate"
)
```

## Setup Instructions

### Step 1: Data Import
1. Open Microsoft Power BI Desktop
2. Click "Get Data" → "Text/CSV"
3. Navigate to the `03_PowerBI_Dashboard/` folder
4. Import the following files:
   - `insurance_data_powerbi.csv` (main dataset)
   - `policy_summary.csv`
   - `monthly_trends.csv`
   - `demographics.csv`
   - `customer_segments.csv`
   - `location_performance.csv`
   - `kpi_metrics.csv`
   - `risk_distribution.csv`

### Step 2: Data Modeling
1. Create relationships between tables:
   - Link `insurance_data_powerbi` to `policy_summary` on Policy Type
   - Link `insurance_data_powerbi` to `demographics` on Age Group and Gender
   - Link `insurance_data_powerbi` to `location_performance` on Location

### Step 3: Calculated Columns
1. Create calculated columns for better analysis:
   - Age Group (if not already present)
   - Income Group (if not already present)
   - Risk Category (if not already present)
   - Policy Duration Years

### Step 4: Calculated Measures
1. Add the DAX measures provided above
2. Create additional measures as needed for specific analysis

### Step 5: Visualizations
1. Create the visualizations as described for each dashboard page
2. Apply consistent formatting and color schemes
3. Add appropriate titles and labels
4. Set up filters and slicers

### Step 6: Formatting
1. Apply corporate color scheme:
   - Primary: #1F4E79 (Dark Blue)
   - Secondary: #D9E2F3 (Light Blue)
   - Accent: #FFC000 (Gold)
   - Success: #70AD47 (Green)
   - Warning: #FFC000 (Orange)
   - Danger: #C5504B (Red)

2. Set consistent fonts:
   - Headers: Segoe UI Bold, 14-16pt
   - Body: Segoe UI Regular, 10-12pt
   - Numbers: Segoe UI Regular, 10-12pt

### Step 7: Interactivity
1. Set up cross-filtering between visualizations
2. Add drill-through capabilities
3. Configure tooltips with additional information
4. Set up bookmarks for different views

## Refresh Settings

### Data Refresh
1. Go to "Data" → "Refresh"
2. Set up automatic refresh schedule:
   - Frequency: Daily
   - Time: 6:00 AM (off-peak hours)
   - Time zone: Local time zone

### Gateway Configuration
1. Set up data gateway for scheduled refreshes
2. Configure credentials for data sources
3. Test connection and refresh

## Performance Optimization

### Data Model Optimization
1. Remove unnecessary columns
2. Use appropriate data types
3. Create calculated columns for frequently used calculations
4. Optimize relationships

### Visualization Optimization
1. Limit data points in visualizations
2. Use appropriate chart types
3. Implement data reduction techniques
4. Optimize for mobile viewing

## Security and Access

### Row-Level Security
1. Implement RLS if needed for data access control
2. Create security roles based on user groups
3. Test security implementation

### Sharing and Publishing
1. Publish to Power BI Service
2. Set up appropriate sharing permissions
3. Configure workspace access
4. Set up app distribution

## Troubleshooting

### Common Issues
1. **Data Refresh Failures**: Check data source connections and credentials
2. **Performance Issues**: Optimize data model and reduce data volume
3. **Visualization Errors**: Check data types and relationships
4. **Filter Issues**: Verify filter relationships and data consistency

### Support Resources
1. Power BI Documentation
2. Community Forums
3. Microsoft Support
4. Internal IT Support

## Maintenance

### Regular Tasks
1. Monitor data refresh status
2. Update visualizations as needed
3. Review and update calculated measures
4. Optimize performance based on usage

### Updates
1. Add new data sources as needed
2. Update calculations for business rule changes
3. Enhance visualizations based on user feedback
4. Implement new features and capabilities

---

**Dashboard Version**: 1.0.0  
**Last Updated**: April 2025  
**Compatible with**: Power BI Desktop 2.100+ and Power BI Service
