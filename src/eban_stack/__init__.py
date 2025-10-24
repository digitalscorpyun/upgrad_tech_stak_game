"""
EBAN-STACK: Budget risk assessment tools.
Bridges tech, policy, and community through responsible financial analysis.
"""

__version__ = "0.1.0"
__author__ = "digitalscorpyun"

from .risk_checks import flag_overdrafts, summary, OverdraftRule
from .explain import explain_row

__all__ = ["flag_overdrafts", "summary", "OverdraftRule", "explain_row"]