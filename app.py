"""Streamlit entrypoint for the Finance Expense Analyzer."""

import streamlit as st


def main() -> None:
    st.set_page_config(page_title="Finance Expense Analyzer", layout="wide")
    st.title("💰 Finance Expense Analyzer")
    st.write("Upload your expense CSV files to begin the analysis.")

    uploaded_files = st.file_uploader("Upload CSV files", type="csv", accept_multiple_files=True)
    if uploaded_files:
        st.success(f"Received {len(uploaded_files)} file(s). Processing coming soon!")


if __name__ == "__main__":
    main()
