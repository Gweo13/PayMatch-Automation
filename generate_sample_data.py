import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

# Invoice dataset
invoices = pd.DataFrame([
    ["INV001", "Andi", "Japanese", "2026-11-01", "2026-11-10", 2500000],
    ["INV002", "Budi", "German", "2026-11-02", "2026-11-12", 3000000],
    ["INV003", "Citra", "Korean", "2026-11-03", "2026-11-13", 1500000],
    ["INV004", "Deni", "Japanese", "2026-11-04", "2026-11-14", 2000000],
    ["INV005", "Eka", "German", "2026-11-05", "2026-11-15", 3500000],
    ["INV006", "Fajar", "Korean", "2026-11-06", "2026-11-16", 1800000],
    ["INV007", "Gita", "Japanese", "2026-11-07", "2026-11-17", 2200000],
    ["INV008", "Hadi", "German", "2026-11-08", "2026-11-18", 2800000],
], columns=[
    "invoice_id", "student_name", "program",
    "invoice_date", "due_date", "total_amount"
])

# Payment dataset
payments = pd.DataFrame([
    ["TRX001", "INV001", "2026-11-02", 2500000, "Bank Transfer"],
    ["TRX002", "INV002", "2026-11-03", 2000000, "Virtual Account"],
    ["TRX003", "INV003", "2026-11-04", 1500000, "QRIS"],
    ["TRX004", "INV004", "2026-11-05", 2500000, "Bank Transfer"],
    ["TRX005", "INV005", "2026-11-06", 3500000, "Virtual Account"],
    ["TRX006", "INV006", "2026-11-07", 900000, "QRIS"],
    ["TRX007", "INV006", "2026-11-08", 900000, "QRIS"],
    ["TRX008", "INV008", "2026-11-09", 2800000, "Bank Transfer"],
    ["TRX008", "INV008", "2026-11-09", 2800000, "Bank Transfer"],
    ["TRX009", "INV999", "2026-11-10", 500000, "QRIS"],
    ["TRX010", "INV001", "2026-11-11", 500000, "QRIS"],
    ["TRX010", "INV002", "2026-11-11", 1000000, "QRIS"],
], columns=[
    "transaction_id", "invoice_id", "payment_date",
    "payment_amount", "payment_method"
])

invoices.to_excel(DATA_DIR / "invoices.xlsx", index=False)
payments.to_excel(DATA_DIR / "payments.xlsx", index=False)

print("Sample datasets generated successfully!")
print(f"Invoices: {len(invoices)} records")
print(f"Payments: {len(payments)} records")