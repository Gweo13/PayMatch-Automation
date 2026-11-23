# PayMatch – Payment Reconciliation Automation

An automated payment reconciliation tool built with Python and Streamlit to match customer payments against invoices, identify payment discrepancies, and generate structured Excel reconciliation reports.

## Overview

Manually reconciling invoices and payment transactions can be time-consuming and prone to human error.

**PayMatch** simplifies this process by automating invoice matching, payment verification, duplicate transaction detection, and exception identification through an interactive dashboard.

The application is designed to help businesses monitor payment status and identify transactions that require further review.

## Key Features

- **Automated Payment Matching** – Match payment transactions against invoice records.
- **Payment Status Classification** – Automatically classify invoices as:
  - MATCHED
  - PARTIAL
  - UNPAID
  - OVERPAID
- **Duplicate Detection** – Identify exact duplicate and conflicting transactions.
- **Unmatched Payment Detection** – Identify payments associated with unknown invoice IDs.
- **Data Validation** – Detect missing fields, invalid values, and duplicate invoice records.
- **Interactive Dashboard** – Monitor reconciliation results through KPI metrics, charts, and detailed tables.
- **Excel Report Generation** – Export reconciliation results into a formatted multi-sheet Excel report.
- **Sample Data Demo** – Explore the application without preparing your own datasets.

## Reconciliation Workflow

1. Upload invoice and payment Excel files or use the built-in sample dataset.
2. Validate and clean the input data.
3. Match payment transactions against invoice records.
4. Calculate total payments and outstanding balances.
5. Identify duplicates, unmatched payments, and data exceptions.
6. Review the reconciliation results through the dashboard.
7. Generate and download the Excel reconciliation report.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| Pandas | Data processing and reconciliation |
| Streamlit | Interactive web dashboard |
| Plotly | Data visualization |
| OpenPyXL | Excel report generation |

## Project Structure

```text
PayMatch-Automation/
├── data/
│   ├── invoices.xlsx
│   └── payments.xlsx
├── modules/
│   ├── processor.py
│   ├── matcher.py
│   └── exporter.py
├── output/
├── .streamlit/
│   └── config.toml
├── app.py
├── generate_sample_data.py
├── test_reconciliation.py
├── requirements.txt
└── README.md
```

## Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/Gweo13/PayMatch-Automation.git
cd PayMatch-Automation
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the environment

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

## Sample Data

PayMatch includes synthetic invoice and payment datasets for demonstration purposes.

You can select the built-in sample data option to explore the reconciliation workflow without uploading external files.

## Excel Report

The generated Excel report contains multiple worksheets:

- **Summary** – Overall reconciliation statistics.
- **Invoice Details** – Invoice-level payment status and outstanding balances.
- **Exact Duplicates** – Transactions identified as exact duplicates.
- **Conflicting Duplicates** – Transaction IDs with inconsistent records.
- **Unmatched Payments** – Payments that cannot be linked to existing invoices.
- **Data Review** – Records requiring validation or manual review.

## Project Purpose

This project was developed as a practical demonstration of Python-based business process automation, data validation, payment reconciliation, exception handling, and automated reporting.

**Note:** This is a portfolio demonstration project using synthetic data. It does not connect to real banking systems or payment gateways.

---

Developed as part of an AI & Automation portfolio.