import pandas as pd

from modules.processor import clean_invoices, clean_payments


# Test invalid invoice data
invoices = pd.DataFrame([
    ["INV001", "Andi", "Japanese", "2026-11-01", "2026-11-10", 2500000],
    ["", "Budi", "German", "2026-11-02", "2026-11-12", 3000000],
    ["INV003", "", "Korean", "invalid-date", "2026-11-13", 0],
    ["INV004", "Deni", "Japanese", "2026-11-04", "2026-11-14", 2000000],
    ["INV004", "Eka", "German", "2026-11-05", "2026-11-15", 3500000],
], columns=[
    "invoice_id", "student_name", "program",
    "invoice_date", "due_date", "total_amount"
])


# Test invalid payment data
payments = pd.DataFrame([
    ["TRX001", "INV001", "2026-11-02", 2500000, "Bank Transfer"],
    ["", "INV002", "2026-11-03", 2000000, "Virtual Account"],
    ["TRX003", "INV003", "2026-11-04", -500000, "QRIS"],
    ["TRX004", "", "invalid-date", 1000000, ""],
], columns=[
    "transaction_id", "invoice_id", "payment_date",
    "payment_amount", "payment_method"
])


cleaned_invoices = clean_invoices(invoices)
cleaned_payments = clean_payments(payments)


print("\n===== INVALID INVOICE TEST =====")
print(cleaned_invoices[
    ["invoice_id", "validation_status", "validation_notes"]
].to_string(index=False))


print("\n===== INVALID PAYMENT TEST =====")
print(cleaned_payments[
    ["transaction_id", "validation_status", "validation_notes"]
].to_string(index=False))