-- SIP Portfolio Planning | MySQL 8+
CREATE TABLE IF NOT EXISTS sip_plans (
    investor_id VARCHAR(12) PRIMARY KEY,
    age_band VARCHAR(10) NOT NULL,
    risk_profile VARCHAR(20) NOT NULL,
    scheme_category VARCHAR(30) NOT NULL,
    monthly_sip_inr DECIMAL(12,2) NOT NULL,
    annual_step_up_pct DECIMAL(5,2) NOT NULL,
    assumed_annual_return_pct DECIMAL(5,2) NOT NULL,
    investment_horizon_years INT NOT NULL,
    target_corpus_inr DECIMAL(15,2) NOT NULL
);

-- 1. Plan mix and average contribution by risk profile.
SELECT risk_profile, COUNT(*) AS plan_count,
       ROUND(AVG(monthly_sip_inr), 2) AS avg_monthly_sip_inr,
       ROUND(AVG(annual_step_up_pct), 2) AS avg_step_up_pct
FROM sip_plans GROUP BY risk_profile ORDER BY plan_count DESC;

-- 2. Scheme category distribution and target corpus.
SELECT scheme_category, COUNT(*) AS plan_count,
       ROUND(AVG(target_corpus_inr), 2) AS avg_target_corpus_inr
FROM sip_plans GROUP BY scheme_category ORDER BY plan_count DESC;

-- 3. Age-band contribution patterns.
SELECT age_band, COUNT(*) AS plan_count,
       ROUND(AVG(monthly_sip_inr), 2) AS avg_monthly_sip_inr,
       ROUND(AVG(investment_horizon_years), 1) AS avg_horizon_years
FROM sip_plans
GROUP BY age_band
ORDER BY FIELD(age_band, '18-25','26-35','36-45','46-55','56+');

-- 4. Plans with the largest target corpus relative to monthly contribution.
SELECT investor_id, risk_profile, scheme_category, monthly_sip_inr,
       annual_step_up_pct, assumed_annual_return_pct,
       investment_horizon_years, target_corpus_inr
FROM sip_plans
ORDER BY target_corpus_inr / NULLIF(monthly_sip_inr, 0) DESC
LIMIT 20;

-- Projection calculations are performed in Python to apply month-by-month
-- compounding and annual step-ups consistently.
