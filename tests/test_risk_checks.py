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


from src.eban_stack import risk_checks

def test_large_withdrawal_rule():
    # example row
    row = {"balance": 1000, "amount": -500}  # 50% withdrawal
    result = risk_checks.large_withdrawal_check(row)
    assert result is True, "Should flag withdrawals >40% of balance"

    row2 = {"balance": 1000, "amount": -300}  # 30% withdrawal
    result2 = risk_checks.large_withdrawal_check(row2)
    assert result2 is False, "Should not flag withdrawals <=40%"
