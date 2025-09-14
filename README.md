# Risk & Policy Analytics Dashboard

## Project Overview

A comprehensive analytics dashboard for modeling insurance policy performance, premiums, and loss ratios using SQL and Python-based ETL scripts. This project includes interactive Power BI visualizations for reserve monitoring, pricing simulations, and capital adequacy scenarios, along with automated Excel reports with advanced formulas for client-style presentations.

## Project Structure

```
Risk & Policy Analytics Dashboard/
├── 01_Python_Scripts/           # Python ETL and analysis scripts
│   ├── data_etl_analysis.py     # Main data processing and analysis
│   ├── powerbi_data_prep.py     # Power BI data preparation
│   ├── excel_automation.py      # Excel report automation
│   └── reserve_monitoring.py    # Reserve monitoring and capital adequacy
├── 02_SQL_Queries/              # SQL queries for database analysis
│   └── insurance_analytics_queries.sql
├── 03_PowerBI_Dashboard/        # Power BI dashboard files and data
├── 04_Excel_Reports/            # Automated Excel reports
├── 05_Data_Analysis/            # Generated analysis outputs
├── 06_Documentation/            # Project documentation
├── Insurance Premium Prediction Dataset.csv  # Source dataset
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## Dataset Information

The project uses an insurance premium prediction dataset with 278,860 records and 20 features:

### Key Features:
- **Demographics**: Age, Gender, Marital Status, Number of Dependents
- **Financial**: Annual Income, Credit Score, Premium Amount
- **Health & Lifestyle**: Health Score, Smoking Status, Exercise Frequency
- **Policy Details**: Policy Type, Previous Claims, Insurance Duration
- **Location & Property**: Location, Property Type
- **Customer Data**: Customer Feedback, Policy Start Date

## Features Implemented

### 1. Data Processing & ETL
- **Comprehensive Data Cleaning**: Handles missing values using intelligent imputation
- **Feature Engineering**: Creates derived features like risk categories, age groups, income brackets
- **Risk Scoring**: Multi-factor risk assessment algorithm
- **Data Validation**: Ensures data quality and consistency

### 2. SQL Analytics
- **Policy Performance Metrics**: Overall portfolio analysis and KPIs
- **Risk Analysis**: Risk category classification and high-risk policy identification
- **Premium Analysis**: Demographics-based premium analysis and trends
- **Loss Ratio Analysis**: Comprehensive loss ratio calculations by various segments
- **Customer Segmentation**: Value-based customer segmentation
- **Reserve Monitoring**: Reserve calculation and adequacy analysis
- **Stress Testing**: Multiple stress test scenarios for capital adequacy

### 3. Power BI Dashboard
- **Executive Dashboard**: Key performance indicators and summary metrics
- **Policy Performance Analysis**: Interactive visualizations by policy type and risk category
- **Risk Analysis**: Risk distribution and high-risk policy monitoring
- **Customer Segmentation**: Demographics and value-based analysis
- **Geographic Analysis**: Location-based performance metrics
- **Reserve Monitoring**: Real-time reserve adequacy tracking

### 4. Excel Automation
- **Executive Summary Report**: Professional KPI dashboard with conditional formatting
- **Detailed Analysis Report**: Multi-sheet comprehensive analysis
- **Client Presentation Report**: Client-ready presentation with charts and recommendations
- **Advanced Formulas**: Automated calculations and conditional formatting
- **Professional Styling**: Corporate-grade formatting and visualizations

### 5. Reserve Monitoring & Capital Adequacy
- **Reserve Calculations**: Multiple methodologies (premium-based, claims-based, risk-adjusted)
- **Stress Testing**: Comprehensive stress test scenarios
- **Capital Adequacy Analysis**: Real-time capital adequacy monitoring
- **Risk-Based Reserves**: Dynamic reserve requirements by risk category
- **IBNR Calculations**: Incurred But Not Reported reserve estimates

## Key Metrics & KPIs

### Portfolio Metrics
- Total Policies: 278,860
- Total Premium Volume: $[Calculated from data]
- Average Premium: $[Calculated from data]
- Overall Loss Ratio: [Calculated from data]
- High-Risk Policy Percentage: [Calculated from data]

### Risk Categories
- **Low Risk**: Risk score ≤ 2
- **Medium Risk**: Risk score 3-4
- **High Risk**: Risk score 5-6
- **Very High Risk**: Risk score > 6

### Reserve Requirements
- Premium-based reserves: 15% of annual premiums
- Claims-based reserves: 3x average annual claims
- Risk-adjusted reserves: Variable by risk category
- IBNR reserves: 5% of annual premiums

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Microsoft Power BI Desktop
- Microsoft Excel 2016 or higher
- SQL database (optional, for running SQL queries)

### Python Dependencies
```bash
pip install -r requirements.txt
```

### Required Packages
- pandas >= 1.5.0
- numpy >= 1.21.0
- matplotlib >= 3.5.0
- seaborn >= 0.11.0
- openpyxl >= 3.0.0
- plotly >= 5.0.0
- scikit-learn >= 1.1.0

## Usage Instructions

### 1. Data Processing
```bash
python 01_Python_Scripts/data_etl_analysis.py
```
This script performs comprehensive data cleaning, feature engineering, and generates analysis visualizations.

### 2. Power BI Data Preparation
```bash
python 01_Python_Scripts/powerbi_data_prep.py
```
This script prepares and exports data specifically formatted for Power BI dashboard consumption.

### 3. Excel Report Generation
```bash
python 01_Python_Scripts/excel_automation.py
```
This script generates automated Excel reports with advanced formulas and professional formatting.

### 4. Reserve Monitoring
```bash
python 01_Python_Scripts/reserve_monitoring.py
```
This script performs reserve monitoring analysis and capital adequacy stress testing.

### 5. SQL Analysis
Execute the SQL queries in `02_SQL_Queries/insurance_analytics_queries.sql` against your database to perform comprehensive policy analysis.

## Output Files

### Generated Analysis Files
- `processed_insurance_data.csv`: Cleaned and processed dataset
- `summary_statistics.csv`: Key performance indicators
- `comprehensive_analysis.png`: Main analysis visualizations
- `correlation_heatmap.png`: Feature correlation analysis
- `detailed_analysis.png`: Detailed analytical charts

### Power BI Files
- `insurance_data_powerbi.csv`: Main dataset for Power BI
- `policy_summary.csv`: Policy performance summary
- `monthly_trends.csv`: Time-series trend data
- `demographics.csv`: Demographics analysis
- `customer_segments.csv`: Customer segmentation data
- `location_performance.csv`: Geographic performance metrics
- `kpi_metrics.csv`: Key performance indicators
- `risk_distribution.csv`: Risk category distribution

### Excel Reports
- `Executive_Summary_Report.xlsx`: Executive dashboard with KPIs
- `Detailed_Analysis_Report.xlsx`: Comprehensive multi-sheet analysis
- `Client_Presentation_Report.xlsx`: Client-ready presentation

### Reserve Monitoring
- `reserve_analysis.csv`: Reserve requirements by risk category
- `stress_test_results.csv`: Stress testing scenario results
- `reserve_recommendations.csv`: Reserve management recommendations
- `capital_adequacy_ratios.csv`: Capital adequacy metrics
- `reserve_monitoring_dashboard.png`: Reserve monitoring visualizations

<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/6f9e89e2-71a3-47ab-a57d-f76fbbedfdac" />
<img width="1919" height="1078" alt="image" src="https://github.com/user-attachments/assets/12b37b3b-0eb8-450d-bacb-911fe7e2d1fb" />
<img width="1197" height="867" alt="image" src="https://github.com/user-attachments/assets/35be9331-aafb-4e6d-947a-282417441bac" />
<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/63e0cd64-76b7-4ccd-8711-90416825b9b6" />



## Key Features & Capabilities

### Advanced Analytics
- **Machine Learning Integration**: Risk scoring algorithms
- **Statistical Analysis**: Comprehensive statistical modeling
- **Predictive Analytics**: Loss ratio predictions and trend analysis
- **Scenario Analysis**: Multiple stress test scenarios

### Business Intelligence
- **Real-time Dashboards**: Interactive Power BI visualizations
- **Automated Reporting**: Scheduled report generation
- **Client Presentations**: Professional Excel reports
- **Executive Summaries**: High-level KPI dashboards

### Risk Management
- **Risk Assessment**: Multi-factor risk scoring
- **Reserve Monitoring**: Real-time reserve adequacy tracking
- **Capital Adequacy**: Stress testing and capital planning
- **Compliance Reporting**: Regulatory compliance metrics

## Technical Architecture

### Data Flow
1. **Data Ingestion**: CSV file processing and validation
2. **Data Cleaning**: Missing value imputation and data quality checks
3. **Feature Engineering**: Derived feature creation and transformation
4. **Analysis Processing**: Statistical analysis and modeling
5. **Visualization**: Chart and dashboard generation
6. **Report Export**: Multi-format report generation

### Technology Stack
- **Backend**: Python (pandas, numpy, scikit-learn)
- **Visualization**: matplotlib, seaborn, plotly
- **Database**: SQL (PostgreSQL/MySQL compatible)
- **BI Tool**: Microsoft Power BI
- **Reporting**: Microsoft Excel with openpyxl
- **Documentation**: Markdown

## Performance Optimization

### Data Processing
- Efficient pandas operations for large datasets
- Memory-optimized data structures
- Parallel processing where applicable
- Chunked processing for very large files

### Visualization
- Optimized chart rendering
- Interactive dashboards for better user experience
- Responsive design for different screen sizes
- Export capabilities for presentations

## Future Enhancements

### Planned Features
- **Real-time Data Integration**: API connections for live data
- **Machine Learning Models**: Advanced predictive modeling
- **Mobile Dashboard**: Mobile-responsive Power BI reports
- **Automated Alerts**: Threshold-based alerting system
- **API Development**: REST API for external integrations

### Scalability Improvements
- **Cloud Deployment**: Azure/AWS deployment options
- **Database Integration**: Direct database connections
- **Microservices Architecture**: Modular service design
- **Containerization**: Docker containerization

## Support & Maintenance

### Documentation
- Comprehensive code documentation
- User guides for each component
- API documentation for integrations
- Troubleshooting guides

### Updates
- Regular feature updates
- Bug fixes and improvements
- Performance optimizations
- Security updates

## License

This project is developed for educational and professional purposes. Please ensure compliance with your organization's data usage policies when working with insurance data.

## Contact

For questions, suggestions, or support regarding this Risk & Policy Analytics Dashboard, please contact the development team.

---

**Project Status**: Complete ✅  
**Last Updated**: April 2025  
**Version**: 1.0.0
