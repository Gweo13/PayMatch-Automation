import pandas as pd

from modules.processor import clean_invoices, clean_payments


invoices = pd.read_excel("data/invoices.xlsx")
payments = pd.read_excel("data/payments.xlsx")

cleaned_invoices = clean_invoices(invoices)
cleaned_payments = clean_payments(payments)

print("\n===== INVOICE VALIDATION =====")
print(cleaned_invoices[
    ["invoice_id", "validation_status", "validation_notes"]
].to_string(index=False))

print("\n===== PAYMENT VALIDATION =====")
print(cleaned_payments[
    ["transaction_id", "validation_status", "validation_notes"]
].to_string(index=False))

print("\n===== VALIDATION SUMMARY =====")
print("Valid Invoices:", (cleaned_invoices["validation_status"] == "VALID").sum())
print("Review Invoices:", (cleaned_invoices["validation_status"] == "REVIEW").sum())
print("Valid Payments:", (cleaned_payments["validation_status"] == "VALID").sum())
print("Review Payments:", (cleaned_payments["validation_status"] == "REVIEW").sum())