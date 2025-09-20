# 💰 Finance Expense Analyzer

<!-- Suggested badges: https://img.shields.io/badge/Python-3.11-blue.svg | https://img.shields.io/badge/License-MIT-green.svg | https://img.shields.io/badge/Streamlit-Deployed-red.svg -->

Take control of your spending with an expense analytics toolkit that feels at home in real-world finance workflows. This project pulls messy bank exports into a clean, interactive Streamlit dashboard so you can understand where every dollar goes.

## ✨ Features
- CSV import that normalizes inconsistent column names
- Rule-based (and future ML-assisted) categorization of transactions
- Monthly and category-level spend analysis with quick summaries
- Interactive charts (pie, bar, line) built with Plotly and Streamlit
- Budget alerts to highlight overspending before it becomes a problem
- Streamlit dashboard for a friendly, shareable experience

## 🗂️ Project Structure
```text
finance-expense-analyzer/
├─ data/
│  ├─ raw/          # original CSV files
│  └─ processed/    # cleaned/normalized files
├─ results/         # reports, charts
├─ src/
│  ├─ __init__.py
│  ├─ analysis.py
│  ├─ budget.py
│  ├─ categorize.py
│  ├─ config.py
│  ├─ exceptions.py
│  ├─ init.py
│  ├─ preprocessing.py
│  ├─ utils_io.py
│  └─ visualization.py
├─ tests/
│  ├─ test_analysis.py
│  ├─ test_categorize.py
│  └─ test_preprocessing.py
└─ app.py
```

## 🚀 Getting Started

### Installation
```bash
git clone https://github.com/Keobu/finance-analyzer.git
cd finance-analyzer
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Usage
```bash
streamlit run app.py
```
Then open the auto-launched URL, upload your CSV exports, and explore your spending insights in real time.

## 📸 Dashboard & Reports
| Section | Preview |
| --- | --- |
| Dashboard Overview | ![Streamlit dashboard placeholder](docs/images/dashboard-placeholder.png) |
| Category Breakdown | ![Category chart placeholder](docs/images/category-chart-placeholder.png) |
| Monthly Trend | ![Monthly trend placeholder](docs/images/monthly-trend-placeholder.png) |

> Replace the placeholders above with real screenshots once the visuals are ready.

## ✅ Testing
```bash
python3 -m pytest
```
Add more focused tests as the data pipelines and Streamlit callbacks evolve.

## 🛣️ Roadmap
1. Phase 1 – Project setup, scaffolding, and CI hooks
2. Phase 2 – Core ingestion, preprocessing, and rule-based categorization
3. Phase 3 – Streamlit dashboard MVP with interactive charts
4. Phase 4 – Documentation polish, tutorials, and sample datasets
5. Phase 5 – Expanded testing strategy and quality gates
6. Phase 6 – Deployment options (Streamlit Cloud, container images)

## 🏷️ Topics
- `finance`
- `data-visualization`
- `pandas`
- `streamlit`
- `personal-finance`
- `data-pipeline`

## 📄 License
This project is released under the [MIT License](LICENSE). Feel free to use it, extend it, and share improvements with the community.
