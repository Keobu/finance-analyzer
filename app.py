import streamlit as st
import pandas as pd
from pathlib import Path

from src.preprocessing import load_csv
from src.categorize import categorize_transactions
from src.analysis import monthly_totals, category_totals, net_balance
from src.visualization import plot_expenses_by_category, plot_monthly_trend
from src.budget import check_budget, BudgetError

# ----------------------------
# STREAMLIT APP CONFIG
# ----------------------------
st.set_page_config(
    page_title="Finance Expense Analyzer",
    layout="wide",
    page_icon="💰"
)

st.title("💰 Finance Expense Analyzer")
st.caption("Analyze your expenses, visualize trends, and track budgets.")

# ----------------------------
# SIDEBAR: Budget settings
# ----------------------------
st.sidebar.header("⚙️ Budget Settings")
budgets = {
    "Groceries": st.sidebar.number_input("Groceries budget (€)", value=300),
    "Transport": st.sidebar.number_input("Transport budget (€)", value=150),
    "Housing": st.sidebar.number_input("Housing budget (€)", value=800),
    "Entertainment": st.sidebar.number_input("Entertainment budget (€)", value=100),
}

# ----------------------------
# MAIN APP: Upload CSV
# ----------------------------
uploaded_file = st.file_uploader("📂 Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        # Load & categorize
        df = load_csv(uploaded_file)
        df = categorize_transactions(df)

        # Tabs navigation
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Summary", "📈 Charts", "🚨 Budget Alerts", "📂 Raw Data"])

        # --- Tab 1: Summary
        with tab1:
            st.subheader("📊 Expense Summary")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Net Balance (€)", f"{net_balance(df):.2f}")
            with col2:
                st.metric("Total Categories", df["category"].nunique())
            with col3:
                st.metric("Transactions", len(df))

            st.write("### Category Totals (€)")
            st.dataframe(category_totals(df))

        # --- Tab 2: Charts
        with tab2:
            st.subheader("📈 Charts")
            col1, col2 = st.columns(2)
            with col1:
                path = plot_expenses_by_category(df)
                st.image(str(path))
            with col2:
                path = plot_monthly_trend(df)
                st.image(str(path))

        # --- Tab 3: Budget Alerts
        with tab3:
            st.subheader("🚨 Budget Alerts")
            try:
                alerts = check_budget(df, budgets)
                for alert in alerts:
                    if "⚠️" in alert:
                        st.error(alert)
                    else:
                        st.success(alert)
            except BudgetError as e:
                st.warning(str(e))

        # --- Tab 4: Raw Data
        with tab4:
            st.subheader("📂 Raw Data")
            st.dataframe(df)

    except Exception as e:
        st.error(f"❌ Error: {e}")

else:
    st.info("Please upload a CSV file to start the analysis.")