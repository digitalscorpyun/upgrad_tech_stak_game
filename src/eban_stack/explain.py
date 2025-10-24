"""
Explanation and interpretability functions for budget risk analysis.
Provides human-readable explanations for risk assessments.
"""

from typing import Dict, Any
import pandas as pd


def explain_row(row: pd.Series) -> str:
    """
    Generate human-readable explanation for a single transaction's overdraft assessment.
    
    Args:
        row: Pandas Series containing transaction data with columns:
            - balance: Current account balance
            - amount: Transaction amount (negative for debits)
            - projected_balance: Calculated balance after transaction
            - overdraft_flag: Boolean indicating overdraft risk
            
    Returns:
        String explanation of the risk assessment for this transaction
        
    Example:
        >>> import pandas as pd
        >>> row = pd.Series({
        ...     'balance': 50, 'amount': -75, 'projected_balance': -25, 
        ...     'overdraft_flag': True
        ... })
        >>> explain_row(row)
        '⚠️ OVERDRAFT RISK: $50 balance + $-75 transaction = $-25 (below $0)'
    """
    balance = row.get('balance', 0)
    amount = row.get('amount', 0)
    projected = row.get('projected_balance', balance + amount)
    is_overdraft = row.get('overdraft_flag', False)
    
    if is_overdraft:
        return (f"⚠️ OVERDRAFT RISK: ${balance:.2f} balance + ${amount:.2f} transaction = "
                f"${projected:.2f} (below $0)")
    else:
        action = "deposit" if amount >= 0 else "withdrawal"
        return (f"✅ SAFE: ${balance:.2f} balance + ${amount:.2f} {action} = "
                f"${projected:.2f} (above $0)")


def explain_summary(total_rows: int, overdraft_count: int) -> str:
    """
    Generate summary explanation for overall risk analysis results.
    
    Args:
        total_rows: Total number of transactions analyzed
        overdraft_count: Number of transactions flagged as overdrafts
        
    Returns:
        String summary of risk analysis results
        
    Example:
        >>> explain_summary(100, 5)
        'Analysis of 100 transactions found 5 potential overdrafts (5.0% risk rate)'
    """
    if total_rows == 0:
        return "No transactions to analyze."
    
    risk_rate = (overdraft_count / total_rows) * 100
    
    if overdraft_count == 0:
        return f"✅ Analysis of {total_rows} transactions found no overdraft risks."
    else:
        return (f"Analysis of {total_rows} transactions found {overdraft_count} "
                f"potential overdrafts ({risk_rate:.1f}% risk rate)")


def generate_recommendations(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Generate actionable recommendations based on risk analysis.
    
    Args:
        df: DataFrame with overdraft analysis results
        
    Returns:
        Dictionary containing personalized recommendations and insights
    """
    overdrafts = df[df.get('overdraft_flag', False)]
    
    recommendations = {
        'priority': 'low',
        'actions': [],
        'insights': []
    }
    
    if len(overdrafts) == 0:
        recommendations['actions'].append("Continue current spending patterns - no immediate risks detected.")
        recommendations['insights'].append("Your transactions show good balance management.")
        return recommendations
    
    # High risk scenario
    if len(overdrafts) > len(df) * 0.2:  # More than 20% overdrafts
        recommendations['priority'] = 'high'
        recommendations['actions'].extend([
            "⚠️ Consider reducing discretionary spending immediately",
            "Review and defer non-essential transactions",
            "Contact your bank about overdraft protection options"
        ])
    else:
        recommendations['priority'] = 'medium'
        recommendations['actions'].extend([
            "Review flagged transactions before proceeding",
            "Consider timing large expenses after deposits clear"
        ])
    
    # Specific insights
    avg_overdraft = overdrafts['projected_balance'].mean() if len(overdrafts) > 0 else 0
    recommendations['insights'].append(
        f"Average projected overdraft amount: ${abs(avg_overdraft):.2f}"
    )
    
    return recommendations