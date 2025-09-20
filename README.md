#  Finance Expense Analyzer

A Python project to analyze personal or business expenses from bank CSV files.  
It categorizes transactions, calculates monthly statistics, and visualizes spending trends.

---

##  Features
- Import and preprocess CSV files (robust to different formats)
- Rule-based (and optional ML-based) categorization
- Monthly and yearly expense analysis
- Interactive charts (pie, bar, line)
- Streamlit dashboard for easy use
- Budget alerts when spending limits are exceeded

---

## 📂 Project Structure
finance-expense-analyzer/
├─ data/         # raw and processed CSV files
├─ results/      # charts and reports
├─ src/          # source code
├─ tests/        # unit tests
└─ app.py        # Streamlit dashboard

---

## ⚙️ Installation
Clone the repository and install dependencies:

```bash
git clone https://github.com/<your-username>/finance-expense-analyzer.git
cd finance-expense-analyzer
pip install -r requirements.txt