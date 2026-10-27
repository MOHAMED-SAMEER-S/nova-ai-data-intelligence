import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import html
import io
import hashlib
import re

# ------------------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------------------
st.set_page_config(
    page_title="NOVA | AI Data Intelligence",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------------------------------------------
# PREMIUM DARK UI — HTML + CSS ANIMATIONS
# ------------------------------------------------------------
st.markdown("""
<style>

:root {
  --bg: #07111f;
  --panel: rgba(12, 27, 45, .82);
  --line: rgba(89, 190, 220, .20);
  --text: #edfaff;
  --muted: #9bb8c9;
  --violet: #7c8cff;
  --cyan: #35e0c1;
  --pink: #ffb86b;
}
html, body, [class*="css"] {
  font-family: 'DM Sans', 'Segoe UI', Arial, sans-serif;
}
.stApp {
  color: var(--text);
  background:
    radial-gradient(ellipse at 12% 8%, rgba(40, 224, 193, .16), transparent 34%),
    radial-gradient(ellipse at 88% 16%, rgba(95, 120, 255, .20), transparent 32%),
    radial-gradient(ellipse at 52% 100%, rgba(255, 184, 107, .08), transparent 40%),
    linear-gradient(145deg, #06101c 0%, #0b1a2b 48%, #07111f 100%);
  background-size: 160% 160%;
  animation: backgroundFlow 24s ease-in-out infinite alternate;
}
.stApp:before {
  content: "";
  position: fixed; inset: 0; pointer-events: none; z-index: 0;
  opacity: .12;
  background-image: radial-gradient(rgba(255,255,255,.35) .65px, transparent .65px);
  background-size: 22px 22px;
  animation: none;
}
@keyframes backgroundFlow { 0% { background-position: 0% 20%; } 50% { background-position: 100% 65%; } 100% { background-position: 20% 100%; } }
@keyframes floatIn { from {opacity:0; transform:translateY(14px)} to {opacity:1; transform:translateY(0)} }
@keyframes glow { 0%,100% { box-shadow: 0 0 18px rgba(53,224,193,.10); } 50% { box-shadow: 0 0 30px rgba(53,224,193,.18); } }
@keyframes gradientMove { 0% {background-position:0% 50%} 100% {background-position:200% 50%} }

.block-container { padding-top: 1.5rem; padding-bottom: 3rem; max-width: 1500px; }
[data-testid="stHeader"] { background: transparent; }
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, rgba(17,22,42,.98), rgba(9,13,26,.98));
  border-right: 1px solid var(--line);
}
[data-testid="stSidebar"] * { color: #dce4ff; }
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { color: #aab6d5; }
h1,h2,h3 { font-family: 'Space Grotesk', 'Segoe UI', Arial, sans-serif !important; letter-spacing: -.035em; }
h1 { font-size: clamp(2.1rem, 4vw, 3.25rem) !important; font-weight: 700 !important; }
h2 { font-size: 1.65rem !important; }
h3 { font-size: 1.15rem !important; }
p, label, span { letter-spacing: .005em; }
.muted { color: var(--muted); }
.eyebrow {
  text-transform: uppercase; letter-spacing: .19em; font-size: .72rem;
  color: var(--cyan); font-weight: 700; margin-bottom: .45rem;
}
.hero {
  position: relative; overflow: hidden; border: 1px solid var(--line);
  border-radius: 26px; padding: 30px 32px; margin-bottom: 24px;
  background: linear-gradient(120deg, rgba(12,37,54,.90), rgba(16,24,55,.78));
  animation: floatIn .7s ease both, glow 8s ease-in-out infinite;
}
.hero:after {
  content:""; position:absolute; width:260px; height:260px; right:-65px; top:-105px;
  background: radial-gradient(circle, rgba(53,224,193,.18), rgba(53,224,193,.10) 40%, transparent 70%);
  border-radius:50%; filter:blur(3px);
}
.hero h1 {
  background: linear-gradient(90deg,#fff,#b8b1ff,#65e7ed,#fff);
  background-size: 200% auto; -webkit-background-clip:text; background-clip:text;
  color: transparent; animation: gradientMove 8s linear infinite;
  margin: 0 0 8px 0;
}
.hero p { color:#aab6d5; max-width:760px; margin-bottom:0; line-height:1.65; }
.hero-chip {
  display:inline-flex; align-items:center; gap:8px; margin-top:18px;
  padding:7px 12px; border:1px solid rgba(86,224,232,.22); border-radius:100px;
  color:#bffaff; background:rgba(86,224,232,.07); font-size:.78rem;
}
.pulse-dot { width:7px;height:7px;border-radius:50%;background:#56e0a4;box-shadow:0 0 12px #56e0a4; }
.section-head { margin: 24px 0 12px; }
.section-head .kicker { color:var(--cyan); text-transform:uppercase; letter-spacing:.16em; font-size:.7rem; font-weight:700; }
.section-head h2 { margin:4px 0 0; }
.kpi {
  min-height:142px; padding:19px 20px; border-radius:20px; position:relative; overflow:hidden;
  border:1px solid var(--line); background:linear-gradient(145deg,rgba(25,32,58,.88),rgba(13,20,37,.86));
  animation:floatIn .65s ease both; transition:transform .25s ease,border-color .25s ease;
}
.kpi:hover { transform:translateY(-4px); border-color:rgba(53,224,193,.60); }
.kpi:after { content:""; position:absolute; right:-24px; bottom:-42px; width:115px;height:115px;
  border-radius:50%; background:radial-gradient(circle,rgba(53,224,193,.17),transparent 70%); }
.kpi-label { color:var(--muted); font-size:.83rem; margin-bottom:12px; }
.kpi-value { color:#f4f6ff; font-family:'Space Grotesk',sans-serif; font-size:clamp(1.5rem,2vw,2rem); font-weight:700; line-height:1.2; }
.kpi-foot { color:#aab6d5; font-size:.76rem; margin-top:9px; }
.kpi-icon { float:right; font-size:1.25rem; opacity:.9; }
.panel {
  padding:20px 21px; border:1px solid var(--line); border-radius:20px;
  background:rgba(16,23,42,.68); margin-bottom:14px;
}
div[data-testid="stVerticalBlockBorderWrapper"] { border-color:var(--line) !important; border-radius:18px; }
.stTabs [data-baseweb="tab-list"] { gap:8px; border-bottom:1px solid var(--line); }
.stTabs [data-baseweb="tab"] { background:rgba(22,29,52,.7); border-radius:10px 10px 0 0; padding:10px 16px; }
.stTabs [aria-selected="true"] { background:rgba(155,140,255,.16) !important; border-bottom:2px solid var(--violet) !important; }
.stButton button, .stDownloadButton button {
  border:1px solid rgba(155,140,255,.42); border-radius:12px; color:#fff;
  background:linear-gradient(110deg,rgba(45,190,173,.95),rgba(88,112,245,.92));
  font-weight:700; transition:all .22s ease;
}
.stButton button:hover, .stDownloadButton button:hover { transform:translateY(-2px); box-shadow:0 8px 24px rgba(103,113,230,.22); border-color:#b9b0ff; color:white; }
.stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"], .stNumberInput input, .stDateInput input {
  background:rgba(8,13,27,.82) !important; border-color:var(--line) !important; color:#eef2ff !important; border-radius:11px !important;
}
[data-testid="stDataFrame"], [data-testid="stTable"] { border:1px solid var(--line); border-radius:14px; overflow:hidden; }
hr { border-color:var(--line); }
div[data-testid="stAlert"] { border-radius:14px; }
div[data-testid="stMetric"] { background:rgba(22,29,52,.65); border:1px solid var(--line); border-radius:15px; padding:14px; }
div[data-testid="stMetricLabel"] { color:var(--muted); }
footer { visibility:hidden; }
#MainMenu { visibility:hidden; }
.app-footer { text-align:center; color:#9aa8c4; font-size:.78rem; padding:28px 0 8px; }
/* FIX-G1: Respect users who prefer reduced motion. */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; scroll-behavior: auto !important; transition-duration: 0.01ms !important; }
}
@media (max-width: 700px) {
  .hero { padding:22px 20px; border-radius:20px; }
  .block-container { padding-left:1rem; padding-right:1rem; }
}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# FREE SMART ANALYTICS ENGINE
# ------------------------------------------------------------
# NOVA FREE SMART ANALYTICS ENGINE
# No API key required.


def _norm_text(value):
    return str(value).strip().lower()

def _find_col(df, candidates):
    """Find a column using case-insensitive aliases."""
    lookup = {_norm_text(c).replace(" ", "_"): c for c in df.columns}
    for candidate in candidates:
        key = _norm_text(candidate).replace(" ", "_")
        if key in lookup:
            return lookup[key]
    return None

def _format_number(value, currency=""):
    try:
        n = float(value)
        if not np.isfinite(n):
            return "not available"
        formatted = f"{n:,.3f}" if currency.upper() == "BHD" else f"{n:,.2f}"
        return f"{formatted} {currency}".strip()
    except Exception:
        return str(value)

# FIX-C2: One shared transaction classifier for all financial calculations.
INCOME_PATTERN = r"\b(?:income|credit|revenue|salary|deposit)\b"
EXPENSE_PATTERN = r"\b(?:expense|debit|payment|cost|withdrawal|purchase)\b"


def _transaction_masks(df, type_col):
    if type_col not in df.columns:
        empty = pd.Series(False, index=df.index, dtype=bool)
        return empty, empty
    values = df[type_col].fillna("").astype(str).str.lower()
    income_mask = values.str.contains(INCOME_PATTERN, regex=True, na=False)
    expense_mask = values.str.contains(EXPENSE_PATTERN, regex=True, na=False)
    return income_mask, expense_mask


def safe_numeric(series):
    """Convert numeric values safely, treating NaN and +/- infinity as missing."""
    values = pd.to_numeric(series, errors="coerce")
    return values.replace([np.inf, -np.inf], np.nan)

def run_smart_analysis(data):
    """
    Produce a structured local analysis from a DataFrame.
    Returns a dictionary with summary, quality report, alerts, recommendations,
    and chart-ready DataFrames.
    """
    if not isinstance(data, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame.")
    if data.empty:
        return {
            "summary": ["The dataset is empty. Upload a CSV or Excel file first."],
            "quality": pd.DataFrame(),
            "alerts": ["No rows are available to analyse."],
            "recommendations": ["Upload a dataset containing records and column headers."],
            "category_summary": pd.DataFrame(),
            "monthly_summary": pd.DataFrame(),
            "outliers": pd.DataFrame(),
            "stats": {},
        }

    df = data.copy()
    amount_col = _find_col(df, ["Amount", "Value", "Total", "Transaction_Amount", "Sales", "Revenue"])
    type_col = _find_col(df, ["Transaction_Type", "Type", "Transaction Type", "Income_Expense"])
    date_col = _find_col(df, ["Date", "Transaction_Date", "Transaction Date", "Created_At"])
    category_col = _find_col(df, ["Category", "Expense_Category", "Product_Category", "Department"])
    currency_col = _find_col(df, ["Currency"])
    currency = "BHD"
    if currency_col and df[currency_col].notna().any():
        currency = str(df[currency_col].dropna().astype(str).mode().iloc[0])

    # Quality report
    quality = pd.DataFrame({
        "Column": list(df.columns),
        "Data type": [str(df[c].dtype) for c in df.columns],
        "Missing count": [int(df[c].isna().sum()) for c in df.columns],
        "Missing %": [round(float(df[c].isna().mean() * 100), 2) for c in df.columns],
        "Unique values": [int(df[c].nunique(dropna=True)) for c in df.columns],
    })
    duplicate_count = int(df.duplicated().sum())
    missing_cells = int(df.isna().sum().sum())

    summary = [
        f"Dataset contains {len(df):,} rows and {len(df.columns)} columns.",
        f"Found {missing_cells:,} missing cells and {duplicate_count:,} duplicate rows.",
    ]
    alerts, recommendations = [], []
    if missing_cells:
        alerts.append(f"Data quality: {missing_cells} missing cell(s) across {int((df.isna().sum() > 0).sum())} column(s).")
        recommendations.append("Review missing values before using results for reporting. Fill values only when the business meaning is clear.")
    if duplicate_count:
        alerts.append(f"Possible duplicates: {duplicate_count} fully duplicated row(s).")
        recommendations.append("Check duplicate rows and remove them only if they are genuinely repeated records.")
    if not missing_cells:
        summary.append("No missing cells detected.")
    if not duplicate_count:
        summary.append("No fully duplicated rows detected.")

    stats = {
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "missing_cells": missing_cells,
        "duplicate_rows": duplicate_count,
        "amount_column": amount_col,
        "type_column": type_col,
        "date_column": date_col,
        "category_column": category_col,
        "currency": currency,
    }
    category_summary = pd.DataFrame()
    monthly_summary = pd.DataFrame()
    outliers = pd.DataFrame()

    if amount_col:
        amounts = pd.to_numeric(df[amount_col], errors="coerce")
        valid = amounts.dropna()
        stats.update({
            "amount_sum": float(valid.sum()) if len(valid) else 0.0,
            "amount_mean": float(valid.mean()) if len(valid) else 0.0,
            "amount_median": float(valid.median()) if len(valid) else 0.0,
            "amount_min": float(valid.min()) if len(valid) else 0.0,
            "amount_max": float(valid.max()) if len(valid) else 0.0,
        })
        summary.append(f"Total of numeric {amount_col} values: {_format_number(valid.sum(), currency)}.")
        if len(valid):
            summary.append(f"Average transaction value: {_format_number(valid.mean(), currency)}; median: {_format_number(valid.median(), currency)}.")
            q1, q3 = valid.quantile([0.25, 0.75])
            iqr = q3 - q1
            if iqr > 0:
                mask = (amounts < q1 - 1.5 * iqr) | (amounts > q3 + 1.5 * iqr)
                outliers = df.loc[mask.fillna(False)].copy()
                if not outliers.empty:
                    alerts.append(f"Unusual values: {len(outliers)} potential outlier row(s) detected with the IQR method.")
                    recommendations.append("Review flagged high/low values against source records; outliers are not automatically errors and were not removed.")
            if valid.nunique() > 1:
                if valid.std(ddof=0) / max(abs(valid.mean()), 1e-9) > 1.5:
                    alerts.append("Amount values vary widely; averages may be influenced by a few large transactions.")
                    recommendations.append("Compare the median with the mean and inspect large transactions before drawing conclusions.")
        else:
            alerts.append(f"Column '{amount_col}' has no valid numeric values.")
            recommendations.append(f"Convert '{amount_col}' to numeric values and review unrecognised text.")
    else:
        alerts.append("No recognised amount/value column was found.")
        recommendations.append("Add a numeric column named Amount, Value, Total, Sales, or Revenue for value analysis.")

    if type_col and amount_col:
        income_mask, expense_mask = _transaction_masks(df, type_col)
        income_total = float(pd.to_numeric(df.loc[income_mask, amount_col], errors="coerce").sum())
        expense_total = float(pd.to_numeric(df.loc[expense_mask, amount_col], errors="coerce").sum())
        net = income_total - expense_total
        stats.update({"income": income_total, "expenses": expense_total, "net_cash_flow": net})
        summary.append(f"Recorded income: {_format_number(income_total, currency)}.")
        summary.append(f"Recorded expenses: {_format_number(expense_total, currency)}.")
        summary.append(f"Estimated net cash flow: {_format_number(net, currency)}.")
        if income_total > 0:
            expense_ratio = expense_total / income_total * 100
            stats["expense_to_income_pct"] = expense_ratio
            if expense_ratio >= 90:
                alerts.append(f"Expenses are {expense_ratio:.1f}% of recorded income.")
                recommendations.append("Review recurring costs and confirm the dataset includes all income and expense records for the same period.")
            elif expense_ratio >= 70:
                alerts.append(f"Expenses are {expense_ratio:.1f}% of recorded income; monitor the trend.")
                recommendations.append("Compare spending month by month and identify categories that could be reduced.")
            else:
                recommendations.append("Compare the expense-to-income ratio across months to see whether the current pattern is consistent.")
        if net < 0:
            alerts.append("Recorded expenses exceed recorded income in the selected dataset.")
            recommendations.append("Check the date range, transaction types, and whether transfers or refunds have been classified correctly.")
        elif net > 0:
            recommendations.append("Review whether the positive net cash flow is consistent across months rather than driven by a one-off income item.")
        if category_col:
            temp = pd.DataFrame({
                "Category": df[category_col].fillna("(Missing category)").astype(str),
                "Amount": pd.to_numeric(df[amount_col], errors="coerce").fillna(0),
                "_type": df[type_col].fillna("").astype(str).str.lower(),
            })
            # Expense category view when there are recognised expense records; otherwise all amounts.
            expense_temp = temp[temp["_type"].str.contains(r"expense|debit|payment|cost|withdrawal|purchase", regex=True)]
            use = expense_temp if not expense_temp.empty else temp
            category_summary = use.groupby("Category", as_index=False)["Amount"].sum().sort_values("Amount", ascending=False)
            if not category_summary.empty:
                top = category_summary.iloc[0]
                summary.append(f"Top category by {'expenses' if not expense_temp.empty else 'total amount'}: {top['Category']} ({_format_number(top['Amount'], currency)}).")
                recommendations.append(f"Inspect '{top['Category']}' transactions to understand what drives its total; a high total may reflect normal recurring needs.")
    elif type_col and not amount_col:
        summary.append("Transaction type exists, but a numeric amount column is needed to calculate income and expenses.")

    if date_col and amount_col:
        dates = pd.to_datetime(df[date_col], errors="coerce")
        dated = pd.DataFrame({
            "Date": dates,
            "Amount": pd.to_numeric(df[amount_col], errors="coerce"),
        }).dropna()
        if not dated.empty:
            dated["Month"] = dated["Date"].dt.to_period("M").astype(str)
            monthly_summary = dated.groupby("Month", as_index=False)["Amount"].sum()
            if len(monthly_summary) >= 2:
                last = monthly_summary.iloc[-1]["Amount"]
                previous = monthly_summary.iloc[-2]["Amount"]
                change = last - previous
                pct = (change / abs(previous) * 100) if previous != 0 else np.nan
                summary.append(
                    f"Latest month total: {_format_number(last, currency)}; previous month: {_format_number(previous, currency)}."
                )
                if np.isfinite(pct):
                    summary.append(f"Month-over-month change in total amount: {pct:+.1f}%.")
                    if pct > 25:
                        alerts.append("Latest monthly total is more than 25% above the previous month.")
                        recommendations.append("Check whether the increase is caused by seasonality, new activity, or a one-off transaction.")
                    elif pct < -25:
                        alerts.append("Latest monthly total is more than 25% below the previous month.")
                        recommendations.append("Check for incomplete recent data, seasonality, or a genuine reduction in activity.")
            else:
                summary.append("Only one month of valid dates is available; a month-over-month comparison needs at least two months.")
        else:
            alerts.append(f"No valid dates were found in '{date_col}'.")
            recommendations.append(f"Check date formats in '{date_col}' to enable time-trend analysis.")

    if not alerts:
        alerts.append("No major quality or financial alert was identified by the built-in checks.")
    if not recommendations:
        recommendations.append("Upload a representative dataset and review the quality report before relying on any conclusions.")

    # Deduplicate repeated advice while preserving order.
    recommendations = list(dict.fromkeys(recommendations))
    return {
        "summary": summary,
        "quality": quality,
        "alerts": alerts,
        "recommendations": recommendations,
        "category_summary": category_summary,
        "monthly_summary": monthly_summary,
        "outliers": outliers,
        "stats": stats,
    }


# FIX-D2: Cache expensive local analytics for the current dataframe content.
@st.cache_data(show_spinner=False, max_entries=8)
def cached_smart_analysis(data_frame):
    return run_smart_analysis(data_frame)

def answer_data_question(question, data, analysis=None):
    """Small local Q&A helper; no network/API call."""
    analysis = analysis if analysis is not None else cached_smart_analysis(data)
    q = re.sub(r"\s+", " ", str(question).lower()).strip()
    s = analysis["stats"]
    currency = s.get("currency", "")
    amount_col = s.get("amount_column")
    type_col = s.get("type_column")

    if any(x in q for x in ["help", "what can you", "example questions"]):
        return ("I can answer questions about row count, columns, missing values, duplicates, "
                "total/average amount, income, expenses, net cash flow, top category, monthly trend, "
                "and unusual transactions. Example: 'What is the net cash flow?'")
    if any(x in q for x in ["how many rows", "row count", "number of records", "how many records"]):
        return f"Your dataset has {s['rows']:,} rows and {s['columns']:,} columns."
    if "column" in q:
        return "Columns detected: " + ", ".join(map(str, data.columns))
    if "missing" in q or "null" in q or "data quality" in q:
        return f"There are {s['missing_cells']:,} missing cells. " + (
            "; ".join(f"{r['Column']}: {r['Missing count']}" for _, r in analysis["quality"].iterrows() if r["Missing count"] > 0)
            if s["missing_cells"] and not analysis["quality"].empty else "No missing cells detected."
        )
    if "duplicate" in q:
        return f"The dataset contains {s['duplicate_rows']:,} fully duplicated rows."
    if any(x in q for x in ["outlier", "unusual", "abnormal", "anomaly"]):
        return f"The IQR method flagged {len(analysis['outliers']):,} potential outlier rows. They are only flags for review, not proof of errors."
    if "recommend" in q or "suggestion" in q or "what should" in q or "improve" in q:
        return "Recommendations:\n" + "\n".join(f"- {x}" for x in analysis["recommendations"])
    if "alert" in q or "risk" in q or "problem" in q:
        return "Alerts:\n" + "\n".join(f"- {x}" for x in analysis["alerts"])
    if any(x in q for x in ["average", "mean", "median"]):
        key = "amount_median" if "median" in q else "amount_mean"
        if key in s:
            return f"{'Median' if key.endswith('median') else 'Average'} amount: {_format_number(s[key], currency)}."
        return "I could not identify a numeric Amount/Value column."
    if "income" in q:
        return f"Recorded income: {_format_number(s.get('income', 0), currency)}." if "income" in s else "I need a recognised transaction type column and numeric amount column to identify income."
    if any(x in q for x in ["expense", "spending", "spent", "cost"]):
        return f"Recorded expenses: {_format_number(s.get('expenses', 0), currency)}." if "expenses" in s else "I need a recognised transaction type column and numeric amount column to identify expenses."
    if any(x in q for x in ["net", "cash flow", "profit", "balance"]):
        return f"Estimated net cash flow (income minus expenses): {_format_number(s['net_cash_flow'], currency)}." if "net_cash_flow" in s else "I need transaction types and amounts to calculate net cash flow."
    if "top category" in q or "category" in q:
        if not analysis["category_summary"].empty:
            top = analysis["category_summary"].iloc[0]
            return f"Top category in the available category view: {top['Category']} — {_format_number(top['Amount'], currency)}."
        return "I could not find usable Category and Amount columns."
    if any(x in q for x in ["month", "trend", "increased", "decreased", "change"]):
        if not analysis["monthly_summary"].empty:
            return "Monthly totals:\n" + "\n".join(
                f"- {r['Month']}: {_format_number(r['Amount'], currency)}"
                for _, r in analysis["monthly_summary"].tail(12).iterrows()
            )
        return "I need valid Date and Amount columns to analyse monthly trends."
    if any(x in q for x in ["largest", "highest", "biggest", "maximum"]):
        if amount_col:
            values = pd.to_numeric(data[amount_col], errors="coerce")
            if values.notna().any():
                idx = values.idxmax()
                row = data.loc[idx]
                details = "; ".join(f"{c}: {row[c]}" for c in data.columns[:6])
                return f"Largest value: {_format_number(values.loc[idx], currency)}. Record details: {details}"
        return "I could not find a valid numeric amount column."
    if any(x in q for x in ["total", "sum"]):
        if "amount_sum" in s:
            return f"Total numeric amount: {_format_number(s['amount_sum'], currency)}."
        return "I could not find a numeric amount column."
    if any(x in q for x in ["summary", "overview", "analyse", "analyze"]):
        return "\n".join(f"- {line}" for line in analysis["summary"])
    return ("I couldn't match that question to a built-in analysis yet. Try: "
            "'summary', 'total amount', 'average amount', 'income', 'expenses', "
            "'net cash flow', 'top category', 'monthly trend', 'missing values', "
            "'outliers', or 'recommendations'.")


# ------------------------------------------------------------
# HELPERS
# ------------------------------------------------------------
def money(value, currency="BHD"):
    try:
        value = float(value)
        return f"{value:,.3f} {currency}" if currency == "BHD" else f"{value:,.2f} {currency}"
    except Exception:
        return "—"

def section(title, kicker="WORKSPACE"):
    # FIX-E1: Escape untrusted text before inserting it into HTML.
    title_safe = html.escape(str(title))
    kicker_safe = html.escape(str(kicker))
    st.markdown(
        f'<div class="section-head"><div class="kicker">{kicker_safe}</div><h2>{title_safe}</h2></div>',
        unsafe_allow_html=True
    )


def kpi(label, value, icon, foot="Live from current dataset"):
    # FIX-E1: Escape all dynamic strings rendered as HTML.
    label, value, icon, foot = [html.escape(str(x)) for x in (label, value, icon, foot)]
    st.markdown(f"""
    <div class="kpi">
      <div class="kpi-icon">{icon}</div>
      <div class="kpi-label">{label}</div>
      <div class="kpi-value">{value}</div>
      <div class="kpi-foot">{foot}</div>
    </div>""", unsafe_allow_html=True)


# FIX-D1/D2: Cache file parsing by content hash and file type.
@st.cache_data(show_spinner=False, max_entries=8)
def _read_uploaded_bytes(file_bytes, filename, excel_sheet=0):
    suffix = str(filename).lower().rsplit(".", 1)[-1]
    if not file_bytes:
        raise ValueError("The uploaded file is empty.")
    if suffix == "csv":
        last_error = None
        for encoding in ("utf-8-sig", "utf-8", "latin-1"):
            try:
                frame = pd.read_csv(io.BytesIO(file_bytes), encoding=encoding)
                if frame.empty and len(frame.columns) == 0:
                    raise ValueError("The CSV does not contain readable columns.")
                return frame
            except UnicodeDecodeError as exc:
                last_error = exc
        raise ValueError("Could not decode this CSV. Save it as UTF-8 and try again.") from last_error
    if suffix in {"xlsx", "xls"}:
        return pd.read_excel(io.BytesIO(file_bytes), sheet_name=excel_sheet)
    raise ValueError("Unsupported file type. Upload a CSV or Excel file.")


def prepare_data(raw, impute_amount=False, drop_duplicates=False, dayfirst=False):
    # FIX-C1/C4/C5/C7: Cleaning is explicit and reports every relevant change.
    if not isinstance(raw, pd.DataFrame):
        raise ValueError("The uploaded data could not be read as a table.")
    if raw.empty or len(raw.columns) == 0:
        raise ValueError("This file contains no usable rows or columns.")
    data = raw.copy()
    data.columns = [str(c).strip().replace(" ", "_") for c in data.columns]
    for col in data.select_dtypes(include=["object", "string"]).columns:
        data[col] = data[col].map(lambda x: x.strip() if isinstance(x, str) else x)
        data[col] = data[col].replace(r"^\s*$", np.nan, regex=True)

    duplicate_count = int(data.duplicated().sum())
    if drop_duplicates:
        data = data.drop_duplicates().copy()

    imputed_counts = {}
    # Identify amount-like columns by name; invalid text becomes missing, not zero.
    for col in data.columns:
        key = str(col).strip().lower().replace("_", " ")
        if key in {"amount", "transaction amount", "sales", "revenue", "income", "value", "total amount"}:
            values = safe_numeric(data[col])
            before = int(values.isna().sum())
            if impute_amount and values.notna().any():
                values = values.fillna(values.median())
            imputed_counts[col] = before - int(values.isna().sum())
            data[col] = values

    date_reports = {}
    for col in data.columns:
        key = str(col).strip().lower().replace("_", " ")
        if key in {"date", "order date", "transaction date", "created at", "timestamp", "datetime"} or key.endswith(" date"):
            original = data[col]
            parsed = pd.to_datetime(original, errors="coerce", dayfirst=dayfirst)
            date_reports[col] = int((original.notna() & parsed.isna()).sum())
            data[col] = parsed

    data.attrs["nova_cleaning_report"] = {
        "duplicate_rows_detected": duplicate_count,
        "duplicates_removed": duplicate_count if drop_duplicates else 0,
        "amount_values_imputed": imputed_counts,
        "unparsed_dates": date_reports,
        "missing_values_remaining": int(data.isna().sum().sum()),
        "rows_after_cleaning": len(data),
    }
    return data, duplicate_count

def infer_currency(data):
    if "Currency" in data.columns and data["Currency"].notna().any():
        return str(data["Currency"].mode().iloc[0])
    return "BHD"

def numeric_summary(data):
    num = data.select_dtypes(include=np.number)
    if num.empty:
        return pd.DataFrame({"Message": ["No numeric columns found."]})
    return num.describe().T.round(3)

# ------------------------------------------------------------
# SIDEBAR
# ------------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div style="padding:12px 4px 22px;">
      <div style="font-size:1.75rem;font-weight:800;font-family:'Space Grotesk',sans-serif;">
        <span style="color:#a99cff;">✦</span> NOVA
      </div>
      <div style="font-size:.72rem;letter-spacing:.18em;color:#8794b8;">AI DATA INTELLIGENCE</div>
    </div>
    """, unsafe_allow_html=True)
    page = st.radio(
        "NAVIGATION",
        ["Overview", "Data Studio", "Financial Insights", "Ask Your Data"],
        index=0,
    )
    st.markdown("---")
    st.markdown("**YOUR DATA**")
    uploaded_file = st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx", "xls"])
    st.caption("Your file is processed in this app session.")
    # FIX-C1/C4/C5/C6: explicit user-controlled cleaning and display settings.
    max_file_mb = st.selectbox("Maximum upload size", [10, 25, 50, 100], index=1, format_func=lambda x: f"{x} MB")
    impute_amount = st.checkbox("Fill missing amount values with median", value=False)
    drop_duplicates = st.checkbox("Remove fully duplicate rows", value=False)
    dayfirst = st.checkbox("Parse dates as day/month/year", value=False)
    currency_setting = st.selectbox("Display currency", ["BHD", "USD", "EUR", "SAR", "AED", "GBP", "INR"], index=0)
    excel_sheet = 0
    if uploaded_file is not None and uploaded_file.name.lower().endswith((".xlsx", ".xls")):
        try:
            xl = pd.ExcelFile(uploaded_file)
            excel_sheet = st.selectbox("Excel sheet", xl.sheet_names, index=0)
            uploaded_file.seek(0)
        except Exception:
            st.warning("Could not read Excel sheet names. Please check that the workbook is valid.")
    st.caption("Your file is processed in this app session.")
    st.markdown("---")
    st.markdown('<div style="color:#aab6d5;font-size:.78rem;">✦ NOVA workspace<br>Built for analytics workflows</div>', unsafe_allow_html=True)

# ------------------------------------------------------------
# LOAD DATA
# ------------------------------------------------------------
# FIX-D1/D2: Validate uploads, cache file parsing, and avoid exposing raw exceptions.
if "raw_df" not in st.session_state:
    st.session_state.raw_df = None
if "clean_df" not in st.session_state:
    st.session_state.clean_df = None
if "cleaning_report" not in st.session_state:
    st.session_state.cleaning_report = None
if "active_upload_key" not in st.session_state:
    st.session_state.active_upload_key = None

if uploaded_file is not None:
    try:
        file_bytes = uploaded_file.getvalue()
        if not file_bytes:
            raise ValueError("The selected file is empty.")
        if len(file_bytes) > int(max_file_mb) * 1024 * 1024:
            raise ValueError(f"File is larger than the selected {max_file_mb} MB limit.")
        file_key = hashlib.sha256(file_bytes).hexdigest() + uploaded_file.name + str(excel_sheet)
        with st.spinner("Loading and preparing your dataset..."):
            if st.session_state.active_upload_key != file_key:
                raw = _read_uploaded_bytes(file_bytes, uploaded_file.name, excel_sheet)
                cleaned, dupes = prepare_data(raw, impute_amount, drop_duplicates, dayfirst)
                report = cleaned.attrs.get("nova_cleaning_report", {})
                st.session_state.raw_df = raw
                st.session_state.clean_df = cleaned
                st.session_state.cleaning_report = {
                    "rows_before": len(raw),
                    "rows_after": len(cleaned),
                    "duplicates_detected": dupes,
                    "duplicates_removed": report.get("duplicates_removed", 0),
                    "missing_remaining": int(cleaned.isna().sum().sum()),
                    "columns": len(cleaned.columns),
                    "amount_values_imputed": report.get("amount_values_imputed", {}),
                    "unparsed_dates": report.get("unparsed_dates", {}),
                }
                st.session_state.active_upload_key = file_key
            else:
                # Re-apply options when a cleaning checkbox changes.
                raw = st.session_state.raw_df.copy()
                cleaned, dupes = prepare_data(raw, impute_amount, drop_duplicates, dayfirst)
                report = cleaned.attrs.get("nova_cleaning_report", {})
                st.session_state.clean_df = cleaned
                st.session_state.cleaning_report = {
                    "rows_before": len(raw), "rows_after": len(cleaned),
                    "duplicates_detected": dupes,
                    "duplicates_removed": report.get("duplicates_removed", 0),
                    "missing_remaining": int(cleaned.isna().sum().sum()),
                    "columns": len(cleaned.columns),
                    "amount_values_imputed": report.get("amount_values_imputed", {}),
                    "unparsed_dates": report.get("unparsed_dates", {}),
                }
    except ValueError as exc:
        st.error(str(exc))
    except Exception:
        st.error("We could not read this file. Check the file format, column headers, and whether the workbook is damaged.")
else:
    # FIX-D3: Removing the upload returns the app to demo data with a visible banner.
    st.session_state.raw_df = None
    st.session_state.clean_df = None
    st.session_state.cleaning_report = None
    st.session_state.active_upload_key = None

# Demo data lets the app work immediately, even before upload.
def demo_data():
    rng = np.random.default_rng(23)
    n = 180
    dates = pd.date_range(end=pd.Timestamp.today().normalize(), periods=n, freq="D")
    types = rng.choice(["Income", "Expense"], size=n, p=[0.32, 0.68])
    categories = rng.choice(
        ["Salary", "Food", "Transport", "Rent", "Shopping", "Utilities", "Freelance", "Healthcare"],
        size=n
    )
    amounts = []
    for t, c in zip(types, categories):
        if t == "Income":
            amounts.append(round(float(rng.uniform(80, 950)), 3))
        else:
            base = {"Rent": 260, "Food": 8, "Transport": 4, "Shopping": 20, "Utilities": 18, "Healthcare": 12}.get(c, 35)
            amounts.append(round(float(rng.uniform(base * .3, base * 1.8)), 3))
    return pd.DataFrame({
        "Transaction_ID": [f"TX-{i+1:04d}" for i in range(n)],
        "Date": dates,
        "Transaction_Type": types,
        "Category": categories,
        "Description": [f"{c} transaction" for c in categories],
        "Amount": amounts,
        "Currency": "BHD",
    })

if st.session_state.raw_df is None:
    st.session_state.raw_df = demo_data()
    st.session_state.clean_df, dupes = prepare_data(st.session_state.raw_df)
    st.session_state.cleaning_report = {
        "rows_before": len(st.session_state.raw_df),
        "rows_after": len(st.session_state.clean_df),
        "duplicates_removed": dupes,
        "missing_remaining": int(st.session_state.clean_df.isna().sum().sum()),
        "columns": len(st.session_state.clean_df.columns),
    }

raw_df = st.session_state.raw_df.copy()
df = st.session_state.clean_df.copy()
if uploaded_file is None:
    st.info("Demo data — upload a CSV or Excel file in the sidebar to analyse your own dataset.")
currency = currency_setting if uploaded_file is not None else infer_currency(df)
has_amount = "Amount" in df.columns
if has_amount:
    amount_series = safe_numeric(df["Amount"]).fillna(0)
else:
    amount_series = pd.Series(np.zeros(len(df)), index=df.index)

# Standardized financial interpretation when expected columns exist.
# FIX-C2: Reuse the same classification logic everywhere.
type_col_global = _find_col(df, ["Transaction_Type", "Type", "Transaction Type", "Income_Expense"])
income_mask, expense_mask = _transaction_masks(df, type_col_global) if type_col_global else _transaction_masks(df, "")

income = float(amount_series[income_mask].sum()) if has_amount else 0.0
expenses = float(amount_series[expense_mask].sum()) if has_amount else 0.0
net = income - expenses
transaction_count = len(df)
avg_amount = float(amount_series.mean()) if len(amount_series) else 0.0

# ------------------------------------------------------------
# GLOBAL HERO
# ------------------------------------------------------------
st.markdown("""
<div class="hero">
  <div class="eyebrow">INTELLIGENCE • ANALYTICS • ACTION</div>
  <h1>AI Data Intelligence</h1>
  <p>Turn raw files into clear decisions. Explore your data, detect quality issues, understand financial performance, and ask questions in plain English — all in one workspace.</p>
  <div class="hero-chip"><span class="pulse-dot"></span> WORKSPACE READY &nbsp;·&nbsp; LIVE SESSION</div>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# OVERVIEW
# ------------------------------------------------------------
if page == "Overview":
    section("Your data at a glance", "EXECUTIVE OVERVIEW")
    # Automatic KPIs adapt to the uploaded dataset instead of assuming a fixed schema.
    numeric_cols = list(df.select_dtypes(include=np.number).columns)
    col_lookup = {str(c).strip().lower().replace("_", " "): c for c in df.columns}
    order_col = next((col_lookup[k] for k in ["order id", "orderid", "order number", "order no", "transaction id", "transaction id "] if k in col_lookup), None)
    amount_col_auto = next((col_lookup[k] for k in ["amount", "sales", "revenue", "total", "price", "value", "transaction amount", "profit"] if k in col_lookup and pd.api.types.is_numeric_dtype(df[col_lookup[k]])), None)
    date_col_auto = next((col_lookup[k] for k in ["date", "order date", "transaction date", "created at"] if k in col_lookup), None)
    unique_ids = int(df[order_col].nunique(dropna=True)) if order_col else None
    total_value = float(pd.to_numeric(df[amount_col_auto], errors="coerce").fillna(0).sum()) if amount_col_auto else None
    avg_value = float(pd.to_numeric(df[amount_col_auto], errors="coerce").dropna().mean()) if amount_col_auto and pd.to_numeric(df[amount_col_auto], errors="coerce").notna().any() else None
    kpis = [("Total records", f"{len(df):,}", "▤", f"{len(df.columns)} columns detected")]
    if income_mask.any() or expense_mask.any():
        kpis += [("Total income", money(income, currency), "↗", "Detected from transaction type"),
                 ("Total expenses", money(expenses, currency), "↘", "Detected from transaction type"),
                 ("Net cash flow", money(net, currency), "✧", "Income minus expenses")]
    else:
        if total_value is not None:
            kpis.append((f"Total {amount_col_auto}", f"{total_value:,.2f}", "↗", "Sum of detected numeric field"))
        if avg_value is not None:
            kpis.append((f"Average {amount_col_auto}", f"{avg_value:,.2f}", "◉", "Average of valid values"))
        if order_col:
            kpis.append(("Unique orders / IDs", f"{unique_ids:,}", "#", f"Detected column: {order_col}"))
        if date_col_auto:
            dates = pd.to_datetime(df[date_col_auto], errors="coerce").dropna()
            if not dates.empty:
                kpis.append(("Date coverage", f"{(dates.max()-dates.min()).days + 1:,} days", "◷", f"{dates.min():%d %b %Y} – {dates.max():%d %b %Y}"))
        if len(kpis) < 4:
            kpis.append(("Numeric columns", f"{len(numeric_cols):,}", "∑", "Detected automatically"))
            kpis.append(("Missing cells", f"{int(df.isna().sum().sum()):,}", "◇", "Across the uploaded dataset"))
    kpis = kpis[:4]
    kpi_cols = st.columns(len(kpis), gap="medium")
    for slot, item in zip(kpi_cols, kpis):
        with slot:
            kpi(*item)

    left, right = st.columns([1.45, 1], gap="large")
    with left:
        section("Cash flow trend", "PERFORMANCE")
        if "Date" in df.columns and has_amount:
            trend = df.copy()
            trend["Date"] = pd.to_datetime(trend["Date"], errors="coerce")
            trend = trend.dropna(subset=["Date"])
            if not trend.empty:
                # FIX-C3: Show income, expense and net separately; use shared masks.
                trend["_income"] = np.where(income_mask.reindex(trend.index, fill_value=False), safe_numeric(trend["Amount"]).fillna(0), 0.0)
                trend["_expense"] = np.where(expense_mask.reindex(trend.index, fill_value=False), safe_numeric(trend["Amount"]).fillna(0), 0.0)
                trend = trend.groupby("Date", as_index=False).agg(Income=("_income", "sum"), Expense=("_expense", "sum"))
                trend["Net"] = trend["Income"] - trend["Expense"]
                fig = px.line(trend, x="Date", y=["Income", "Expense", "Net"], markers=True)
                fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                  margin=dict(l=5,r=5,t=15,b=5), height=320,
                                  xaxis_title=None, yaxis_title=f"Amount ({currency})")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Date values could not be interpreted. Check the Date column in Data Studio.")
        else:
            st.info("Upload a dataset with Date and Amount columns to see the cash-flow trend.")

    with right:
        section("Category breakdown", "CATEGORY MIX")
        if "Category" in df.columns and has_amount:
            cat = df.assign(_amount=amount_series).groupby("Category", dropna=False)["_amount"].sum().reset_index().sort_values("_amount", ascending=False).head(9)
            fig = px.pie(cat, names="Category", values="_amount", hole=.68)
            fig.update_traces(textposition="inside", textinfo="percent", marker=dict(line=dict(color="#101629", width=2)))
            fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                              margin=dict(l=0,r=0,t=12,b=0), height=320, showlegend=True,
                              legend=dict(font=dict(size=10)))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Add Category and Amount columns to see the category mix.")

    # Order / transaction ID frequency panel. Frequency is computed on up to 5,000 rows
    # for responsive performance on large spreadsheets; this cap is adjustable in the UI.
    id_col = next((c for c in df.columns if str(c).strip().lower().replace("_", " ") in
                   {"orderid", "order id", "order number", "order no", "transaction id", "invoice id", "customer id"}), None)
    if id_col:
        section("Order ID frequency", "ORDER INTELLIGENCE")
        f1, f2 = st.columns([1, 3], gap="large")
        with f1:
            row_limit = st.selectbox("Rows to analyse", [5000, 10000, 25000, "All rows"], index=0, key="frequency_row_limit")
            top_n = st.selectbox("Show top IDs", [5, 10, 20, 50], index=1, key="frequency_top_n")
        frequency_source = df.head(len(df) if row_limit == "All rows" else min(int(row_limit), len(df)))
        frequency = frequency_source[id_col].dropna().astype(str).value_counts().head(int(top_n)).rename_axis(id_col).reset_index(name="Frequency")
        with f2:
            if not frequency.empty:
                fig = px.bar(frequency.sort_values("Frequency"), x="Frequency", y=id_col, orientation="h",
                             color="Frequency", color_continuous_scale=["#35e0c1", "#6478ff", "#ffb86b"])
                fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                  height=max(280, 28 * len(frequency) + 90), margin=dict(l=5,r=8,t=10,b=5),
                                  coloraxis_showscale=False, xaxis_title="Frequency", yaxis_title=None)
                st.plotly_chart(fig, use_container_width=True)
                st.caption(f"Analysed {len(frequency_source):,} rows from **{id_col}**. Frequency is calculated from actual values; IDs are not artificially changed.")
            else:
                st.info("No non-empty IDs found in this column.")

    section("Recent records", "DATA PREVIEW")
    st.dataframe(df.head(12), use_container_width=True, hide_index=True)
    st.caption("The Overview page uses a sample dataset until you upload your own file in the sidebar.")

# ------------------------------------------------------------
# DATA STUDIO
# ------------------------------------------------------------
elif page == "Data Studio":
    section("Explore & clean your dataset", "DATA QUALITY LAB")
    st.markdown('<div class="panel">Review detected columns, missing values, duplicate rows, and data types. Cleaning is applied to a working copy; download the result when you are ready.</div>', unsafe_allow_html=True)
    q1, q2, q3, q4 = st.columns(4)
    report = st.session_state.cleaning_report or {}
    with q1: st.metric("Rows after cleaning", f"{len(df):,}")
    with q2: st.metric("Columns", f"{len(df.columns):,}")
    with q3: st.metric("Duplicates removed", f"{report.get('duplicates_removed', 0):,}")
    with q4: st.metric("Missing cells remaining", f"{int(df.isna().sum().sum()):,}")
    st.caption(f"Fully duplicated rows detected: {report.get('duplicates_detected', report.get('duplicates_removed', 0)):,} · Removed: {report.get('duplicates_removed', 0):,}")
    imputed = report.get("amount_values_imputed", {})
    if imputed:
        st.caption("Amount values imputed: " + ", ".join(f"{html.escape(str(k))}: {v}" for k, v in imputed.items()))
    unparsed = report.get("unparsed_dates", {})
    if unparsed:
        st.caption("Unparsed dates: " + ", ".join(f"{html.escape(str(k))}: {v}" for k, v in unparsed.items()))

    tab1, tab2, tab3 = st.tabs(["Dataset preview", "Quality report", "Statistics"])
    with tab1:
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.download_button("⬇ Download cleaned CSV", df.to_csv(index=False).encode("utf-8"), "nova_cleaned_data.csv", "text/csv")
    with tab2:
        quality = pd.DataFrame({
            "Column": df.columns,
            "Data type": [str(df[c].dtype) for c in df.columns],
            "Missing values": [int(df[c].isna().sum()) for c in df.columns],
            "Missing %": [round(float(df[c].isna().mean() * 100), 2) for c in df.columns],
            "Unique values": [int(df[c].nunique(dropna=True)) for c in df.columns],
        })
        st.dataframe(quality, use_container_width=True, hide_index=True)
        if quality["Missing values"].sum() == 0:
            st.success("No missing cells remain in the cleaned dataset.")
        else:
            st.warning("Some missing values remain in columns other than Amount. Review the report before using the data.")
    with tab3:
        st.dataframe(numeric_summary(df), use_container_width=True)
        if has_amount:
            st.markdown("**Amount distribution**")
            fig = px.histogram(df, x="Amount", nbins=28, marginal="box")
            fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=330)
            st.plotly_chart(fig, use_container_width=True)

# ------------------------------------------------------------
# FINANCIAL INSIGHTS
# ------------------------------------------------------------
elif page == "Financial Insights":
    section("Financial performance", "FINANCIAL INTELLIGENCE")
    if not has_amount:
        st.warning("Your dataset needs an Amount column for financial analysis.")
    else:
        a, b, c, d = st.columns(4)
        with a: st.metric("Income", money(income, currency))
        with b: st.metric("Expenses", money(expenses, currency))
        with c: st.metric("Net cash flow", money(net, currency))
        with d: st.metric("Average transaction", money(avg_amount, currency))

        if "Transaction_Type" in df.columns:
            st.markdown('<div class="panel"><b>AI-style summary</b><br>', unsafe_allow_html=True)
            if income > 0 and expenses > 0:
                ratio = expenses / income * 100
                if net > 0:
                    st.write(f"Your recorded income exceeds expenses by **{money(net, currency)}**. Expenses are approximately **{ratio:.1f}%** of recorded income.")
                elif net < 0:
                    st.write(f"Recorded expenses exceed income by **{money(abs(net), currency)}**. Review recurring costs and large transactions.")
                else:
                    st.write("Recorded income and expenses are currently balanced.")
                if ratio > 80:
                    st.write("**Watch-out:** Expenses are above 80% of income in this dataset. Check whether one-off transactions are affecting the result.")
                elif ratio < 50:
                    st.write("**Positive signal:** Recorded expenses are below half of income. Check the date range and confirm all transactions are included.")
            else:
                st.write("The app could not identify both income and expense transactions. Check values in the Transaction_Type column (for example, Income and Expense).")
            st.markdown("</div>", unsafe_allow_html=True)

        if "Category" in df.columns:
            cat = df.assign(_amount=amount_series).groupby("Category", dropna=False)["_amount"].sum().reset_index().sort_values("_amount", ascending=False)
            l, r = st.columns(2, gap="large")
            with l:
                section("Amount by category", "CATEGORY ANALYSIS")
                fig = px.bar(cat, x="Category", y="_amount", color="_amount", color_continuous_scale=["#35e0c1", "#6478ff", "#ffb86b"])
                fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=360,
                                  xaxis_title=None, yaxis_title=f"Amount ({currency})", coloraxis_showscale=False)
                st.plotly_chart(fig, use_container_width=True)
            with r:
                section("Largest transactions", "OUTLIER REVIEW")
                largest = df.assign(_amount=amount_series).sort_values("_amount", ascending=False).head(10)
                st.dataframe(largest, use_container_width=True, hide_index=True)
                if len(amount_series) >= 4:
                    q1v, q3v = amount_series.quantile([.25, .75])
                    iqr = q3v - q1v
                    outliers = df[(amount_series < q1v - 1.5 * iqr) | (amount_series > q3v + 1.5 * iqr)]
                    st.caption(f"IQR method flagged {len(outliers)} potential outlier row(s). Outliers are not automatically removed.")

        if "Date" in df.columns:
            dated = df.copy()
            dated["Date"] = pd.to_datetime(dated["Date"], errors="coerce")
            dated = dated.dropna(subset=["Date"])
            if not dated.empty:
                dated["Month"] = dated["Date"].dt.to_period("M").astype(str)
                dated["_amount"] = safe_numeric(dated["Amount"]).fillna(0)
                dated_income = income_mask.reindex(dated.index, fill_value=False)
                dated_expense = expense_mask.reindex(dated.index, fill_value=False)
                dated["Income"] = np.where(dated_income, dated["_amount"], 0.0)
                dated["Expense"] = np.where(dated_expense, dated["_amount"], 0.0)
                monthly = dated.groupby("Month", as_index=False).agg(Income=("Income", "sum"), Expense=("Expense", "sum"))
                monthly["Net"] = monthly["Income"] - monthly["Expense"]
                section("Monthly movement", "TIME SERIES")
                fig = px.line(monthly, x="Month", y=["Income", "Expense", "Net"], markers=True)
                fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=320,
                                  xaxis_title=None, yaxis_title=f"Amount ({currency})")
                st.plotly_chart(fig, use_container_width=True)

# ------------------------------------------------------------
# ASK YOUR DATA — no paid API needed
# ------------------------------------------------------------
elif page == "Ask Your Data":
    section("Ask questions in plain English", "DATA COPILOT")
    st.markdown('<div class="panel">This built-in assistant uses local rules and your current dataset. It does not require an API key. Try: <i>total income</i>, <i>total expenses</i>, <i>top category</i>, <i>average amount</i>, <i>largest transaction</i>, or <i>how many rows</i>.</div>', unsafe_allow_html=True)
    suggestions = ["How many rows?", "Total income", "Total expenses", "Net cash flow", "Average amount", "Top category", "Largest transaction", "Show columns", "Missing values", "Find outliers", "Monthly trend", "Recommendations"]
    cols = st.columns(4)
    for i, suggestion in enumerate(suggestions):
        with cols[i % 4]:
            if st.button(suggestion, key=f"suggest_{i}", use_container_width=True):
                st.session_state.ask_prompt = suggestion

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "ask_prompt" not in st.session_state:
        st.session_state.ask_prompt = ""

    def answer_question(question, data):
        return answer_data_question(question, data, cached_smart_analysis(data))

    # Smart local insights panel — no external AI service or API key.
    smart_report = cached_smart_analysis(df)
    with st.expander("✦ Smart dataset scan — alerts & recommendations", expanded=True):
        st.markdown("**Quick summary**")
        for line in smart_report["summary"]:
            st.write("• " + line)
        left_alert, right_recommend = st.columns(2)
        with left_alert:
            st.markdown("**Alerts to review**")
            for item in smart_report["alerts"]:
                st.warning(item)
        with right_recommend:
            st.markdown("**Recommended next actions**")
            for item in smart_report["recommendations"]:
                st.info(item)
        if not smart_report["quality"].empty:
            st.markdown("**Column quality**")
            st.dataframe(smart_report["quality"], use_container_width=True, hide_index=True)

    for item in st.session_state.chat_history:
        with st.chat_message(item["role"]):
            st.markdown(item["content"])

    prompt = st.chat_input("Ask something about your dataset…")
    if st.session_state.ask_prompt:
        prompt = st.session_state.ask_prompt
        st.session_state.ask_prompt = ""
    if prompt:
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        reply = answer_question(prompt, df)
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.markdown(reply)
    if st.button("Clear conversation"):
        st.session_state.chat_history = []
        st.rerun()

# ------------------------------------------------------------
# FOOTER
# ------------------------------------------------------------
st.markdown("""
<div class="app-footer">
  ✦ NOVA DATA INTELLIGENCE &nbsp;·&nbsp; ANALYZE CLEARLY. DECIDE CONFIDENTLY.<br>
  <span style="opacity:.7;">Prototype analytics assistant — verify outputs before making financial decisions.</span>
</div>
""", unsafe_allow_html=True)
