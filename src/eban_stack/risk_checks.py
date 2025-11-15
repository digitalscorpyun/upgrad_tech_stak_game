"""
Risk assessment functions for budget analysis.
Provides overdraft detection and financial risk flagging capabilities.
"""

from dataclasses import dataclass
from typing import Dict, Any
import pandas as pd


@dataclass
class OverdraftRule:
    """Configuration for overdraft detection rules.
    
    Attributes:
        balance_col: Column name containing current balance
        tx_col: Column name containing transaction amount
    """
    balance_col: str = "balance"
    tx_col: str = "amount"


def flag_overdrafts(df: pd.DataFrame, rule: OverdraftRule = OverdraftRule()) -> pd.DataFrame:
    """
    Flag transactions that would result in account overdrafts.
    
    Args:
        df: DataFrame containing balance and transaction data
        rule: OverdraftRule configuration object
        
    Returns:
        DataFrame with added columns:
        - projected_balance: balance + amount for each transaction  
        - overdraft_flag: True if projected balance < 0
        
    Example:
        >>> df = pd.DataFrame({"balance": [100, 50], "amount": [-20, -60]})
        >>> result = flag_overdrafts(df)
        >>> result["overdraft_flag"].tolist()
        [False, True]
    """
    out = df.copy()
    out["projected_balance"] = out[rule.balance_col] + out[rule.tx_col]
    out["overdraft_flag"] = out["projected_balance"] < 0
    return out


def summary(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Generate summary statistics for risk analysis results.
    
    Args:
        df: DataFrame with overdraft analysis results
        
    Returns:
        Dictionary containing:
        - rows: Total number of transactions analyzed
        - overdrafts: Number of transactions flagged as overdrafts
        
    Example:
        >>> df = pd.DataFrame({"overdraft_flag": [True, False, True]})
        >>> summary(df)
        {'rows': 3, 'overdrafts': 2}
    """
    return {
        "rows": len(df),
        "overdrafts": int(df.get("overdraft_flag", pd.Series(dtype=bool)).sum()),
    }

def flag_large_withdrawals(df: pd.DataFrame, threshold: float = 0.4, 
                           balance_col: str = "balance", tx_col: str = "amount") -> pd.DataFrame:
    """
    Flag transactions where the withdrawal exceeds a given fraction of the balance.

    Args:
        df: DataFrame containing balances and transaction amounts
        threshold: Fraction of balance that triggers a large withdrawal (default 0.4)
        balance_col: Column name for balance
        tx_col: Column name for transaction amount

    Returns:
        DataFrame with added column:
        - large_withdrawal_flag: True if abs(amount) > threshold * balance
    """
    out = df.copy()
    # Only flag withdrawals (negative amounts)
    out["large_withdrawal_flag"] = (out[tx_col] < 0) & (abs(out[tx_col]) > threshold * out[balance_col])
    return out
