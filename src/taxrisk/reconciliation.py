"""Deterministic cross-table checks used by the smoke test."""
import pandas as pd


def reconcile_revenue(accounting: pd.DataFrame, filing: pd.DataFrame, key: str = "period", tolerance: float = 0.01) -> pd.DataFrame:
    required = {key, "revenue"}
    for name, frame in (("accounting", accounting), ("filing", filing)):
        missing = required - set(frame.columns)
        if missing:
            raise ValueError(f"{name} missing columns: {sorted(missing)}")
    result = accounting[[key, "revenue"]].rename(columns={"revenue": "accounting_revenue"}).merge(
        filing[[key, "revenue"]].rename(columns={"revenue": "filing_revenue"}), on=key, how="outer"
    )
    result["difference"] = result["accounting_revenue"] - result["filing_revenue"]
    result["status"] = result["difference"].abs().le(tolerance).map({True: "CLEARED", False: "ANOMALY"})
    return result

