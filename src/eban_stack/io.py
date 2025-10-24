"""
Input/Output utilities for EBAN-STACK budget analysis.
Handles data loading, validation, and export functions.
"""

from typing import Optional, List, Dict, Any
import pandas as pd
import csv
from pathlib import Path


def load_budget_data(file_path: str, required_columns: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Load and validate budget data from CSV file.
    
    Args:
        file_path: Path to CSV file containing budget data
        required_columns: List of required column names to validate
        
    Returns:
        Validated DataFrame with budget data
        
    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If required columns are missing
        
    Example:
        >>> df = load_budget_data("budget.csv", ["balance", "amount"])
        >>> print(df.columns.tolist())
        ['balance', 'amount', 'description']
    """
    if required_columns is None:
        required_columns = ["balance", "amount"]
    
    if not Path(file_path).exists():
        raise FileNotFoundError(f"Budget file not found: {file_path}")
    
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        raise ValueError(f"Error reading CSV file: {e}")
    
    # Validate required columns
    missing_cols = set(required_columns) - set(df.columns)
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")
    
    # Basic data validation
    if df.empty:
        raise ValueError("Budget file is empty")
    
    # Ensure numeric columns are properly typed
    for col in required_columns:
        if col in ["balance", "amount"]:
            try:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            except:
                raise ValueError(f"Column '{col}' contains non-numeric data")
    
    return df


def save_analysis_results(df: pd.DataFrame, output_path: str, include_explanations: bool = True) -> None:
    """
    Save risk analysis results to CSV file.
    
    Args:
        df: DataFrame with analysis results
        output_path: Path where to save the results
        include_explanations: Whether to include human-readable explanations
        
    Example:
        >>> save_analysis_results(analyzed_df, "results.csv")
    """
    output_df = df.copy()
    
    if include_explanations and 'explain_text' not in output_df.columns:
        from .explain import explain_row
        output_df['explain_text'] = output_df.apply(explain_row, axis=1)
    
    # Ensure output directory exists
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    # Save with proper formatting
    output_df.to_csv(output_path, index=False, float_format='%.2f')


def generate_sample_data(num_rows: int = 25, output_path: Optional[str] = None) -> pd.DataFrame:
    """
    Generate synthetic budget data for testing and demonstration.
    
    Args:
        num_rows: Number of sample transactions to generate
        output_path: Optional path to save the sample data
        
    Returns:
        DataFrame with synthetic budget data
        
    Example:
        >>> sample_df = generate_sample_data(10)
        >>> print(sample_df.shape)
        (10, 3)
    """
    import random
    import numpy as np
    
    # Set seed for reproducible results
    random.seed(42)
    np.random.seed(42)
    
    # Generate realistic budget scenarios
    transactions = []
    current_balance = 1000.0  # Starting balance
    
    transaction_types = [
        ("Grocery Store", (-150, -50)),
        ("Salary Deposit", (1500, 3000)),
        ("Rent Payment", (-1200, -800)),
        ("Gas Station", (-80, -30)),
        ("Online Purchase", (-200, -25)),
        ("ATM Withdrawal", (-300, -50)),
        ("Restaurant", (-120, -15)),
        ("Utility Bill", (-200, -75)),
        ("Coffee Shop", (-25, -5)),
        ("Transfer In", (100, 500))
    ]
    
    for i in range(num_rows):
        # Choose transaction type
        desc, (min_amt, max_amt) = random.choice(transaction_types)
        amount = round(random.uniform(min_amt, max_amt), 2)
        
        # Add some balance variation
        if i > 0:
            current_balance = max(0, current_balance + random.uniform(-100, 100))
        
        transactions.append({
            'balance': round(current_balance, 2),
            'amount': amount,
            'description': f"{desc} #{i+1}"
        })
    
    df = pd.DataFrame(transactions)
    
    if output_path:
        df.to_csv(output_path, index=False)
    
    def load_transactions(path: Union[str, Path]) -> pd.DataFrame:
        """
        Load transaction CSV into a Pandas DataFrame.

        Args:
            path: Path to CSV file or file-like object

        Returns:
            DataFrame with transaction data
        """
        return pd.read_csv(path)


    def save_transactions(df: pd.DataFrame, path: Union[str, Path]) -> None:
        """
        Save transaction DataFrame to CSV.

        Args:
            df: DataFrame to save
            path: Destination CSV path
        """
        df.to_csv(path, index=False)
    return df


def validate_data_quality(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Perform data quality checks on budget data.
    
    Args:
        df: DataFrame to validate
        
    Returns:
        Dictionary with validation results and recommendations
    """
    quality_report = {
        'passed': True,
        'warnings': [],
        'errors': [],
        'stats': {}
    }
    
    # Check for missing values
    missing_data = df.isnull().sum()
    if missing_data.any():
        quality_report['warnings'].append(f"Missing data found: {missing_data.to_dict()}")
    
    # Check for duplicate rows
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        quality_report['warnings'].append(f"{duplicates} duplicate rows found")
    
    # Validate balance column
    if 'balance' in df.columns:
        negative_balances = (df['balance'] < 0).sum()
        if negative_balances > 0:
            quality_report['warnings'].append(f"{negative_balances} rows with negative starting balance")
    
    # Validate amount column
    if 'amount' in df.columns:
        zero_amounts = (df['amount'] == 0).sum()
        if zero_amounts > 0:
            quality_report['warnings'].append(f"{zero_amounts} transactions with zero amount")
    
    # Generate basic statistics
    quality_report['stats'] = {
        'total_rows': len(df),
        'columns': list(df.columns),
        'data_types': df.dtypes.to_dict()
    }
    
    if 'balance' in df.columns:
        quality_report['stats']['balance_range'] = (df['balance'].min(), df['balance'].max())
    
    if 'amount' in df.columns:
        quality_report['stats']['amount_range'] = (df['amount'].min(), df['amount'].max())
    
    return quality_report