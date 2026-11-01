# SIP & Mutual Fund Analytics | Step-up Planning Model

A reproducible portfolio project that models illustrative Systematic Investment Plan (SIP) scenarios, estimates projected corpus, and solves for the starting monthly SIP required to reach a target under an assumed return and annual contribution step-up.

> **Data and evidence disclosure:** All records in this repository are synthetic and generated for demonstration. No client, employer, or investor records are included. This is a portfolio recreation inspired by the CV's stated SIP and mutual-fund analytics work. The CV reports a 40% improvement in investment-tracking accuracy; this project does not validate or claim that historical result. This model is educational, not investment advice or a return forecast.

## Business question

Given a starting monthly SIP, annual contribution step-up, assumed annual return, and investment horizon, what corpus does the model project? Conversely, what starting SIP would be required to reach a target under the same assumptions?

## What it demonstrates

- Python-based monthly cash-flow modelling and input validation
- Step-up SIP future-value projection with monthly compounding
- Numerical target solving using bisection
- MySQL exploratory analysis by risk profile, scheme category, and age band
- Reproducible synthetic data and automated CSV outputs
- Unit tests for core calculation behaviours

## Repository structure

```text
sip-mutual-fund-analytics/
├── data/sip_plans_synthetic.csv
├── reports/                  # generated outputs
├── sql/analysis_queries.sql
├── src/analyze_sip.py
├── tests_test_analyze_sip.py
└── requirements.txt
```

## Dataset

The CSV contains 500 synthetic SIP plan records. Each row represents an illustrative plan, not an actual investor.

| Field | Description |
|---|---|
| investor_id | Synthetic plan identifier |
| age_band | Illustrative investor age band |
| risk_profile | Conservative, Moderate, or Aggressive label |
| scheme_category | Illustrative mutual-fund category |
| monthly_sip_inr | Starting monthly contribution in INR |
| annual_step_up_pct | Annual contribution increase applied every 12 months |
| assumed_annual_return_pct | Modelling assumption, not a guaranteed return |
| investment_horizon_years | Projection period |
| target_corpus_inr | Illustrative target corpus |

Risk labels and return assumptions are synthetic descriptors, not recommended or expected returns for any fund category.

## Calculation methodology

1. Convert the effective annual return assumption to an equivalent monthly rate: `(1 + annual_return)^(1/12) - 1`.
2. Treat contributions as occurring at month-end.
3. Increase the monthly contribution once every 12 months by the selected step-up percentage.
4. Compound the balance monthly after each contribution.
5. Solve the required starting SIP using bisection.

The model excludes expense ratios, taxes, exit loads, inflation, contribution interruptions, fund-specific performance, and sequence-of-return uncertainty. Actual investment outcomes can differ materially.

## Run locally

Requires Python 3.10+.

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python src/analyze_sip.py
```

Generated outputs:
- `reports/sip_projection_results.csv` — plan-level projected corpus, target gap, modelled status, and required starting SIP.
- `reports/segment_summary.csv` — aggregate results by risk profile and scheme category.

Run tests:

```bash
python -m unittest discover -s . -p 'tests_*.py' -v
```

## SQL analysis

The schema and MySQL 8+ exploratory queries are in `sql/analysis_queries.sql`. Load the source CSV into a table named `sip_plans`, then execute the queries. Month-by-month projection is implemented in Python so the same compounding and step-up logic is reused for forward projection and target solving.

## CV alignment and evidence boundary

This is a public portfolio recreation inspired by the CV's stated work on SIP and mutual-fund scorecards and Power BI/Tableau dashboards. The CV's 40% investment-tracking accuracy improvement is a historical CV claim; it is not reproduced or validated by this synthetic dataset.

## Future extension

Build a Power BI report from `reports/sip_projection_results.csv` with KPI cards for plan count, average projected corpus, modelled target-hit rate, and required SIP; add slicers for age band, risk profile, and scheme category.
