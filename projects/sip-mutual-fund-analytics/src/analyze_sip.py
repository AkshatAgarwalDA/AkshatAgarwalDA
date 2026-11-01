"""Reproducible SIP projection and target-planning analysis."""
from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np
import pandas as pd

REQUIRED = {"investor_id", "age_band", "risk_profile", "scheme_category",
            "monthly_sip_inr", "annual_step_up_pct", "assumed_annual_return_pct",
            "investment_horizon_years", "target_corpus_inr"}

def future_value_sip(monthly_sip: float, annual_return_pct: float,
                     years: int, annual_step_up_pct: float = 0.0) -> float:
    """Future value of month-end SIPs; step-up is applied every 12 months."""
    if monthly_sip < 0 or years < 0 or annual_return_pct <= -100 or annual_step_up_pct <= -100:
        raise ValueError("Invalid input: SIP and years must be non-negative; rates must exceed -100%.")
    monthly_rate = (1 + annual_return_pct / 100) ** (1 / 12) - 1
    step = annual_step_up_pct / 100
    balance = 0.0
    for month in range(1, years * 12 + 1):
        contribution = monthly_sip * ((1 + step) ** ((month - 1) // 12))
        balance = balance * (1 + monthly_rate) + contribution
    return balance

def required_starting_sip(target: float, annual_return_pct: float,
                          years: int, annual_step_up_pct: float = 0.0) -> float:
    """Find the starting monthly SIP that reaches target using bisection."""
    if target < 0:
        raise ValueError("Target must be non-negative.")
    if target == 0:
        return 0.0
    low, high = 0.0, max(target / max(years * 12, 1), 1.0)
    while future_value_sip(high, annual_return_pct, years, annual_step_up_pct) < target:
        high *= 2
    for _ in range(80):
        mid = (low + high) / 2
        if future_value_sip(mid, annual_return_pct, years, annual_step_up_pct) < target:
            low = mid
        else:
            high = mid
    return high

def run(input_csv: Path, output_dir: Path) -> pd.DataFrame:
    df = pd.read_csv(input_csv)
    missing = REQUIRED - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    numeric = ["monthly_sip_inr", "annual_step_up_pct", "assumed_annual_return_pct",
               "investment_horizon_years", "target_corpus_inr"]
    if df[numeric].isna().any().any():
        raise ValueError("Numeric input columns contain missing values.")
    df["projected_corpus_inr"] = df.apply(
        lambda r: future_value_sip(r.monthly_sip_inr, r.assumed_annual_return_pct,
                                   int(r.investment_horizon_years), r.annual_step_up_pct), axis=1)
    df["target_gap_inr"] = df["projected_corpus_inr"] - df["target_corpus_inr"]
    df["target_status"] = np.where(df["target_gap_inr"] >= 0, "On track (modelled)", "Below target (modelled)")
    df["required_starting_sip_inr"] = df.apply(
        lambda r: required_starting_sip(r.target_corpus_inr, r.assumed_annual_return_pct,
                                        int(r.investment_horizon_years), r.annual_step_up_pct), axis=1)
    output_dir.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_dir / "sip_projection_results.csv", index=False)
    summary = df.groupby(["risk_profile", "scheme_category"], as_index=False).agg(
        plans=("investor_id", "count"),
        avg_monthly_sip_inr=("monthly_sip_inr", "mean"),
        avg_projected_corpus_inr=("projected_corpus_inr", "mean"),
        modelled_target_hit_rate=("target_status", lambda s: (s == "On track (modelled)").mean()))
    summary.to_csv(output_dir / "segment_summary.csv", index=False)
    print(f"Analysed {len(df):,} synthetic SIP plans")
    print(f"Modelled target hit rate: {(df.target_status == 'On track (modelled)').mean():.1%}")
    print(f"Outputs written to: {output_dir.resolve()}")
    return df

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=Path("data/sip_plans_synthetic.csv"))
    parser.add_argument("--output", type=Path, default=Path("reports"))
    args = parser.parse_args()
    run(args.input, args.output)
