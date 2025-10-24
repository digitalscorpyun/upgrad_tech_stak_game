import streamlit as st
import pandas as pd
from pathlib import Path
from typing import Optional

from eban_stack.risk_checks import flag_overdrafts, summary, OverdraftRule
from eban_stack.explain import explain_row, explain_summary
from eban_stack.io import load_budget_data, save_analysis_results


st.set_page_config(page_title="EBAN Budget Guardian", layout="centered")

st.title("EBAN Budget Guardian")
st.caption("Advisory tool only. For education — not financial advice. See Policy → Disclaimers.")

uploaded = st.file_uploader("Upload CSV (columns: balance, amount)", type=["csv"])

if uploaded:
    try:
        # Use load_budget_data for validation; fall back to pandas directly
        try:
            df = load_budget_data(uploaded)
        except Exception:
            df = pd.read_csv(uploaded)

        # Run risk checks
        out = flag_overdrafts(df)

        # Add explanations per row
        out = out.reset_index(drop=True)
        out["explain_text"] = out.apply(explain_row, axis=1)

        # Display results
        st.subheader("Results")
        st.dataframe(out.head(50))

        s = summary(out)
        st.metric("Rows", s["rows"])
        st.metric("Projected overdrafts", s["overdrafts"]) 

        # Summary text
        st.write(explain_summary(s["rows"], s["overdrafts"]))

        # Download
        csv_bytes = out.to_csv(index=False).encode("utf-8")
        st.download_button("Download flagged CSV", csv_bytes, file_name="flagged.csv", mime="text/csv")

        # Save option
        if st.button("Save results to disk"):
            out_path = Path.cwd() / "data" / "processed" / "flagged_results.csv"
            out_path.parent.mkdir(parents=True, exist_ok=True)
            save_analysis_results(out, str(out_path))
            st.success(f"Saved results to {out_path}")

    except Exception as e:
        st.error(f"Error processing file: {e}")

with st.expander("How to read this"):
    st.write("- **projected_balance** = balance + amount for each row.")
    st.write("- **overdraft_flag** = True when projected balance falls below 0.")
    st.write("This tool may be wrong; verify with your bank and do not rely solely on it.")
