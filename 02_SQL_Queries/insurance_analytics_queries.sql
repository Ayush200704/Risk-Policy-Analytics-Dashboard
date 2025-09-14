-- Risk & Policy Analytics Dashboard - SQL Queries
-- Author: Data Analyst
-- Date: April 2025
-- Purpose: Comprehensive SQL queries for insurance policy performance analysis

-- =====================================================
-- 1. BASIC POLICY PERFORMANCE METRICS
-- =====================================================

-- Overall portfolio summary
SELECT 
    COUNT(*) as total_policies,
    SUM(premium_amount) as total_premium_volume,
    AVG(premium_amount) as average_premium,
    MEDIAN(premium_amount) as median_premium,
    SUM(previous_claims) as total_claims,
    AVG(previous_claims) as average_claims_per_policy,
    SUM(previous_claims * 1000) / SUM(premium_amount) as overall_loss_ratio
FROM insurance_policies;

-- Policy performance by type
SELECT 
    policy_type,
    COUNT(*) as policy_count,
    SUM(premium_amount) as total_premiums,
    AVG(premium_amount) as avg_premium,
    SUM(previous_claims) as total_claims,
    AVG(previous_claims) as avg_claims,
    SUM(previous_claims * 1000) / SUM(premium_amount) as loss_ratio,
    COUNT(CASE WHEN previous_claims > 0 THEN 1 END) * 100.0 / COUNT(*) as claim_frequency_pct
FROM insurance_policies
GROUP BY policy_type
ORDER BY total_premiums DESC;

-- =====================================================
-- 2. RISK ANALYSIS QUERIES
-- =====================================================

-- Risk category analysis
WITH risk_categories AS (
    SELECT 
        *,
        CASE 
            WHEN age < 25 OR age > 65 THEN 2
            WHEN age BETWEEN 25 AND 35 THEN 1
            ELSE 0
        END +
        CASE 
            WHEN previous_claims > 2 THEN 3
            WHEN previous_claims > 0 THEN 1
            ELSE 0
        END +
        CASE 
            WHEN health_score < 20 THEN 2
            WHEN health_score < 40 THEN 1
            ELSE 0
        END +
        CASE 
            WHEN credit_score < 500 THEN 2
            WHEN credit_score < 650 THEN 1
            ELSE 0
        END +
        CASE WHEN smoking_status = 'Yes' THEN 2 ELSE 0 END +
        CASE WHEN exercise_frequency = 'Rarely' THEN 1 ELSE 0 END as risk_score
    FROM insurance_policies
),
risk_classification AS (
    SELECT 
        *,
        CASE 
            WHEN risk_score <= 2 THEN 'Low'
            WHEN risk_score <= 4 THEN 'Medium'
            WHEN risk_score <= 6 THEN 'High'
            ELSE 'Very High'
        END as risk_category
    FROM risk_categories
)
SELECT 
    risk_category,
    COUNT(*) as policy_count,
    AVG(premium_amount) as avg_premium,
    AVG(previous_claims) as avg_claims,
    SUM(previous_claims * 1000) / SUM(premium_amount) as loss_ratio,
    AVG(age) as avg_age,
    AVG(health_score) as avg_health_score,
    AVG(credit_score) as avg_credit_score
FROM risk_classification
GROUP BY risk_category
ORDER BY 
    CASE risk_category 
        WHEN 'Low' THEN 1 
        WHEN 'Medium' THEN 2 
        WHEN 'High' THEN 3 
        WHEN 'Very High' THEN 4 
    END;

-- High-risk policy identification
SELECT 
    policy_id,
    age,
    gender,
    policy_type,
    premium_amount,
    previous_claims,
    health_score,
    credit_score,
    smoking_status,
    exercise_frequency,
    risk_category
FROM (
    SELECT 
        ROW_NUMBER() OVER (ORDER BY id) as policy_id,
        *,
        CASE 
            WHEN age < 25 OR age > 65 THEN 2
            WHEN age BETWEEN 25 AND 35 THEN 1
            ELSE 0
        END +
        CASE 
            WHEN previous_claims > 2 THEN 3
            WHEN previous_claims > 0 THEN 1
            ELSE 0
        END +
        CASE 
            WHEN health_score < 20 THEN 2
            WHEN health_score < 40 THEN 1
            ELSE 0
        END +
        CASE 
            WHEN credit_score < 500 THEN 2
            WHEN credit_score < 650 THEN 1
            ELSE 0
        END +
        CASE WHEN smoking_status = 'Yes' THEN 2 ELSE 0 END +
        CASE WHEN exercise_frequency = 'Rarely' THEN 1 ELSE 0 END as risk_score
    FROM insurance_policies
) risk_calc
WHERE risk_score > 6
ORDER BY risk_score DESC, premium_amount DESC
LIMIT 100;

-- =====================================================
-- 3. PREMIUM ANALYSIS QUERIES
-- =====================================================

-- Premium analysis by demographics
SELECT 
    age_group,
    gender,
    marital_status,
    COUNT(*) as policy_count,
    AVG(premium_amount) as avg_premium,
    MEDIAN(premium_amount) as median_premium,
    STDDEV(premium_amount) as premium_stddev,
    MIN(premium_amount) as min_premium,
    MAX(premium_amount) as max_premium
FROM (
    SELECT 
        *,
        CASE 
            WHEN age < 25 THEN '18-24'
            WHEN age < 35 THEN '25-34'
            WHEN age < 45 THEN '35-44'
            WHEN age < 55 THEN '45-54'
            WHEN age < 65 THEN '55-64'
            ELSE '65+'
        END as age_group
    FROM insurance_policies
)
GROUP BY age_group, gender, marital_status
ORDER BY age_group, gender, marital_status;

-- Premium trends by location and property type
SELECT 
    location,
    property_type,
    COUNT(*) as policy_count,
    AVG(premium_amount) as avg_premium,
    SUM(premium_amount) as total_premiums,
    AVG(previous_claims) as avg_claims,
    SUM(previous_claims * 1000) / SUM(premium_amount) as loss_ratio
FROM insurance_policies
GROUP BY location, property_type
ORDER BY total_premiums DESC;

-- Income vs Premium analysis
SELECT 
    income_bracket,
    COUNT(*) as policy_count,
    AVG(premium_amount) as avg_premium,
    AVG(premium_amount / annual_income) as premium_to_income_ratio,
    AVG(previous_claims) as avg_claims
FROM (
    SELECT 
        *,
        CASE 
            WHEN annual_income < 30000 THEN 'Low Income'
            WHEN annual_income < 60000 THEN 'Lower Middle'
            WHEN annual_income < 100000 THEN 'Middle Income'
            WHEN annual_income < 200000 THEN 'Upper Middle'
            ELSE 'High Income'
        END as income_bracket
    FROM insurance_policies
    WHERE annual_income IS NOT NULL
)
GROUP BY income_bracket
ORDER BY 
    CASE income_bracket
        WHEN 'Low Income' THEN 1
        WHEN 'Lower Middle' THEN 2
        WHEN 'Middle Income' THEN 3
        WHEN 'Upper Middle' THEN 4
        WHEN 'High Income' THEN 5
    END;

-- =====================================================
-- 4. LOSS RATIO AND CLAIMS ANALYSIS
-- =====================================================

-- Loss ratio analysis by policy characteristics
SELECT 
    policy_type,
    location,
    CASE 
        WHEN age < 30 THEN 'Young'
        WHEN age < 50 THEN 'Middle-aged'
        ELSE 'Senior'
    END as age_category,
    COUNT(*) as policy_count,
    SUM(premium_amount) as total_premiums,
    SUM(previous_claims * 1000) as estimated_claims,
    SUM(previous_claims * 1000) / SUM(premium_amount) as loss_ratio,
    COUNT(CASE WHEN previous_claims > 0 THEN 1 END) * 100.0 / COUNT(*) as claim_frequency
FROM insurance_policies
GROUP BY policy_type, location, 
    CASE 
        WHEN age < 30 THEN 'Young'
        WHEN age < 50 THEN 'Middle-aged'
        ELSE 'Senior'
    END
HAVING COUNT(*) >= 10  -- Only include segments with sufficient data
ORDER BY loss_ratio DESC;

-- Claims frequency and severity analysis
SELECT 
    policy_type,
    AVG(previous_claims) as avg_claims_per_policy,
    COUNT(CASE WHEN previous_claims = 0 THEN 1 END) * 100.0 / COUNT(*) as no_claims_pct,
    COUNT(CASE WHEN previous_claims = 1 THEN 1 END) * 100.0 / COUNT(*) as one_claim_pct,
    COUNT(CASE WHEN previous_claims = 2 THEN 1 END) * 100.0 / COUNT(*) as two_claims_pct,
    COUNT(CASE WHEN previous_claims > 2 THEN 1 END) * 100.0 / COUNT(*) as multiple_claims_pct,
    AVG(premium_amount) as avg_premium
FROM insurance_policies
GROUP BY policy_type
ORDER BY avg_claims_per_policy DESC;

-- =====================================================
-- 5. CUSTOMER SEGMENTATION QUERIES
-- =====================================================

-- Customer value segmentation
WITH customer_value AS (
    SELECT 
        *,
        premium_amount * insurance_duration as lifetime_value,
        ROW_NUMBER() OVER (ORDER BY premium_amount * insurance_duration DESC) as value_rank
    FROM insurance_policies
),
value_segments AS (
    SELECT 
        *,
        CASE 
            WHEN value_rank <= COUNT(*) OVER () * 0.2 THEN 'High Value'
            WHEN value_rank <= COUNT(*) OVER () * 0.5 THEN 'Medium Value'
            ELSE 'Low Value'
        END as value_segment
    FROM customer_value
)
SELECT 
    value_segment,
    COUNT(*) as customer_count,
    AVG(lifetime_value) as avg_lifetime_value,
    AVG(premium_amount) as avg_premium,
    AVG(previous_claims) as avg_claims,
    AVG(age) as avg_age,
    COUNT(CASE WHEN smoking_status = 'Yes' THEN 1 END) * 100.0 / COUNT(*) as smoking_pct
FROM value_segments
GROUP BY value_segment
ORDER BY avg_lifetime_value DESC;

-- Customer retention analysis
SELECT 
    insurance_duration,
    COUNT(*) as policy_count,
    AVG(premium_amount) as avg_premium,
    AVG(previous_claims) as avg_claims,
    COUNT(CASE WHEN customer_feedback = 'Good' THEN 1 END) * 100.0 / COUNT(*) as good_feedback_pct,
    COUNT(CASE WHEN customer_feedback = 'Poor' THEN 1 END) * 100.0 / COUNT(*) as poor_feedback_pct
FROM insurance_policies
WHERE customer_feedback IS NOT NULL
GROUP BY insurance_duration
ORDER BY insurance_duration;

-- =====================================================
-- 6. PRICING AND RESERVE ANALYSIS QUERIES
-- =====================================================

-- Reserve calculation by risk category
WITH risk_assessment AS (
    SELECT 
        *,
        CASE 
            WHEN age < 25 OR age > 65 THEN 2
            WHEN age BETWEEN 25 AND 35 THEN 1
            ELSE 0
        END +
        CASE 
            WHEN previous_claims > 2 THEN 3
            WHEN previous_claims > 0 THEN 1
            ELSE 0
        END +
        CASE 
            WHEN health_score < 20 THEN 2
            WHEN health_score < 40 THEN 1
            ELSE 0
        END +
        CASE 
            WHEN credit_score < 500 THEN 2
            WHEN credit_score < 650 THEN 1
            ELSE 0
        END +
        CASE WHEN smoking_status = 'Yes' THEN 2 ELSE 0 END +
        CASE WHEN exercise_frequency = 'Rarely' THEN 1 ELSE 0 END as risk_score
    FROM insurance_policies
),
risk_categories AS (
    SELECT 
        *,
        CASE 
            WHEN risk_score <= 2 THEN 'Low'
            WHEN risk_score <= 4 THEN 'Medium'
            WHEN risk_score <= 6 THEN 'High'
            ELSE 'Very High'
        END as risk_category
    FROM risk_assessment
)
SELECT 
    risk_category,
    COUNT(*) as policy_count,
    SUM(premium_amount) as total_premiums,
    AVG(premium_amount) as avg_premium,
    SUM(previous_claims * 1000) as estimated_claims,
    SUM(previous_claims * 1000) / SUM(premium_amount) as loss_ratio,
    -- Reserve calculation (simplified)
    SUM(premium_amount) * 0.15 as required_reserves,  -- 15% of premiums as reserves
    SUM(previous_claims * 1000) as actual_claims,
    SUM(premium_amount) * 0.15 - SUM(previous_claims * 1000) as reserve_surplus_deficit
FROM risk_categories
GROUP BY risk_category
ORDER BY 
    CASE risk_category 
        WHEN 'Low' THEN 1 
        WHEN 'Medium' THEN 2 
        WHEN 'High' THEN 3 
        WHEN 'Very High' THEN 4 
    END;

-- Pricing adequacy analysis
SELECT 
    policy_type,
    location,
    COUNT(*) as policy_count,
    AVG(premium_amount) as avg_premium,
    AVG(previous_claims * 1000) as avg_claims,
    AVG(previous_claims * 1000) / AVG(premium_amount) as loss_ratio,
    -- Pricing adequacy indicators
    CASE 
        WHEN AVG(previous_claims * 1000) / AVG(premium_amount) < 0.6 THEN 'Underpriced'
        WHEN AVG(previous_claims * 1000) / AVG(premium_amount) > 0.8 THEN 'Overpriced'
        ELSE 'Adequately Priced'
    END as pricing_status,
    -- Recommended premium adjustment
    AVG(premium_amount) * (1 + (AVG(previous_claims * 1000) / AVG(premium_amount) - 0.7)) as recommended_premium
FROM insurance_policies
GROUP BY policy_type, location
HAVING COUNT(*) >= 5  -- Only include segments with sufficient data
ORDER BY loss_ratio DESC;

-- =====================================================
-- 7. CAPITAL ADEQUACY SCENARIOS
-- =====================================================

-- Stress testing scenarios
WITH base_metrics AS (
    SELECT 
        SUM(premium_amount) as total_premiums,
        SUM(previous_claims * 1000) as total_claims,
        COUNT(*) as total_policies
    FROM insurance_policies
),
scenarios AS (
    SELECT 
        'Base Case' as scenario,
        total_premiums,
        total_claims,
        total_claims / total_premiums as loss_ratio,
        total_premiums * 0.15 as required_capital
    FROM base_metrics
    
    UNION ALL
    
    SELECT 
        'Stress Test 1: 20% Claims Increase' as scenario,
        total_premiums,
        total_claims * 1.2,
        (total_claims * 1.2) / total_premiums as loss_ratio,
        total_premiums * 0.15 as required_capital
    FROM base_metrics
    
    UNION ALL
    
    SELECT 
        'Stress Test 2: 50% Claims Increase' as scenario,
        total_premiums,
        total_claims * 1.5,
        (total_claims * 1.5) / total_premiums as loss_ratio,
        total_premiums * 0.15 as required_capital
    FROM base_metrics
    
    UNION ALL
    
    SELECT 
        'Stress Test 3: 100% Claims Increase' as scenario,
        total_premiums,
        total_claims * 2.0,
        (total_claims * 2.0) / total_premiums as loss_ratio,
        total_premiums * 0.15 as required_capital
    FROM base_metrics
)
SELECT 
    scenario,
    total_premiums,
    total_claims,
    ROUND(loss_ratio, 4) as loss_ratio,
    required_capital,
    total_claims - required_capital as capital_adequacy,
    CASE 
        WHEN total_claims <= required_capital THEN 'Adequate'
        ELSE 'Inadequate'
    END as capital_status
FROM scenarios
ORDER BY 
    CASE scenario
        WHEN 'Base Case' THEN 1
        WHEN 'Stress Test 1: 20% Claims Increase' THEN 2
        WHEN 'Stress Test 2: 50% Claims Increase' THEN 3
        WHEN 'Stress Test 3: 100% Claims Increase' THEN 4
    END;

-- =====================================================
-- 8. MONTHLY TREND ANALYSIS
-- =====================================================

-- Monthly premium and claims trends
SELECT 
    EXTRACT(YEAR FROM policy_start_date) as year,
    EXTRACT(MONTH FROM policy_start_date) as month,
    COUNT(*) as new_policies,
    SUM(premium_amount) as monthly_premiums,
    AVG(premium_amount) as avg_premium,
    SUM(previous_claims) as monthly_claims,
    AVG(previous_claims) as avg_claims_per_policy
FROM insurance_policies
WHERE policy_start_date IS NOT NULL
GROUP BY EXTRACT(YEAR FROM policy_start_date), EXTRACT(MONTH FROM policy_start_date)
ORDER BY year, month;

-- =====================================================
-- 9. CUSTOMER FEEDBACK ANALYSIS
-- =====================================================

-- Customer satisfaction analysis
SELECT 
    customer_feedback,
    COUNT(*) as response_count,
    COUNT(*) * 100.0 / SUM(COUNT(*)) OVER () as response_pct,
    AVG(premium_amount) as avg_premium,
    AVG(previous_claims) as avg_claims,
    AVG(age) as avg_age,
    COUNT(CASE WHEN smoking_status = 'Yes' THEN 1 END) * 100.0 / COUNT(*) as smoking_pct
FROM insurance_policies
WHERE customer_feedback IS NOT NULL
GROUP BY customer_feedback
ORDER BY 
    CASE customer_feedback
        WHEN 'Excellent' THEN 1
        WHEN 'Good' THEN 2
        WHEN 'Average' THEN 3
        WHEN 'Poor' THEN 4
    END;

-- =====================================================
-- 10. EXECUTIVE SUMMARY QUERIES
-- =====================================================

-- Executive dashboard summary
SELECT 
    'Total Policies' as metric,
    COUNT(*)::text as value
FROM insurance_policies

UNION ALL

SELECT 
    'Total Premium Volume',
    '$' || ROUND(SUM(premium_amount), 2)::text
FROM insurance_policies

UNION ALL

SELECT 
    'Average Premium',
    '$' || ROUND(AVG(premium_amount), 2)::text
FROM insurance_policies

UNION ALL

SELECT 
    'Overall Loss Ratio',
    ROUND(SUM(previous_claims * 1000) / SUM(premium_amount), 4)::text
FROM insurance_policies

UNION ALL

SELECT 
    'High-Risk Policies (%)',
    ROUND(COUNT(CASE WHEN 
        (age < 25 OR age > 65) AND 
        (previous_claims > 1 OR health_score < 30 OR credit_score < 600)
        THEN 1 END) * 100.0 / COUNT(*), 2)::text || '%'
FROM insurance_policies

UNION ALL

SELECT 
    'Customer Satisfaction (Good+)',
    ROUND(COUNT(CASE WHEN customer_feedback IN ('Good', 'Excellent') THEN 1 END) * 100.0 / 
          COUNT(CASE WHEN customer_feedback IS NOT NULL THEN 1 END), 2)::text || '%'
FROM insurance_policies;
