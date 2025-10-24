import pandas as pd
from eban_stack.risk_checks import flag_overdrafts, summary


def test_flag_overdrafts():
    df = pd.DataFrame({"balance":[10,5], "amount":[-3,-9]})
    out = flag_overdrafts(df)
    assert out["overdraft_flag"].tolist() == [False, True]
    s = summary(out)
    assert s["rows"] == 2 and s["overdrafts"] == 1


def test_with_sample_csv(tmp_path):
    # Load sample CSV and ensure we can flag overdrafts
    sample = pd.read_csv("tests/sample_budget.csv")
    out = flag_overdrafts(sample)
    s = summary(out)
    assert s["rows"] == len(sample)
    # Ensure at least one overdraft exists in sample
    assert s["overdrafts"] >= 1
