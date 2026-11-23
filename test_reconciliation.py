import pandas as pd

from modules.processor import clean_invoices, clean_payments
from modules.matcher import reconcile_payments
from modules.exporter import export_reconciliation_report


# ==========================================
# 1. LOAD DATA
# ==========================================

invoices = pd.read_excel("data/invoices.xlsx")
payments = pd.read_excel("data/payments.xlsx")


# ==========================================
# 2. CLEAN AND VALIDATE
# ==========================================

invoices = clean_invoices(invoices)
payments = clean_payments(payments)


# ==========================================
# 3. SEPARATE VALID AND REVIEW DATA
# ==========================================

valid_invoices = invoices[
    invoices["validation_status"] == "VALID"
].drop(columns=["validation_status", "validation_notes"])

review_invoices = invoices[
    invoices["validation_status"] == "REVIEW"
].copy()

valid_payments = payments[
    payments["validation_status"] == "VALID"
].drop(columns=["validation_status", "validation_notes"])

review_payments = payments[
    payments["validation_status"] == "REVIEW"
].copy()


# ==========================================
# 4. RUN RECONCILIATION
# ==========================================

result, exact_duplicates, conflicting_duplicates, unmatched = (
    reconcile_payments(valid_invoices, valid_payments)
)


# ==========================================
# 5. DISPLAY SUMMARY
# ==========================================

print("\n===== PAYMATCH RECONCILIATION =====")

print(f"Total Invoices       : {len(invoices)}")
print(f"Valid Invoices       : {len(valid_invoices)}")
print(f"Invoice Review       : {len(review_invoices)}")

print(f"\nTotal Payments       : {len(payments)}")
print(f"Valid Payments       : {len(valid_payments)}")
print(f"Payment Review       : {len(review_payments)}")

print("\n===== RECONCILIATION SUMMARY =====")

print(f"Matched              : {(result['reconciliation_status'] == 'MATCHED').sum()}")
print(f"Partial              : {(result['reconciliation_status'] == 'PARTIAL').sum()}")
print(f"Unpaid               : {(result['reconciliation_status'] == 'UNPAID').sum()}")
print(f"Overpaid             : {(result['reconciliation_status'] == 'OVERPAID').sum()}")

print(f"\nExact Duplicates     : {len(exact_duplicates)}")
print(f"Conflicting Duplicates: {len(conflicting_duplicates)}")
print(f"Unmatched Payments   : {len(unmatched)}")


# ==========================================
# 6. DISPLAY RECONCILIATION DETAILS
# ==========================================

print("\n===== RECONCILIATION DETAILS =====")

print(
    result[
        [
            "invoice_id",
            "student_name",
            "total_amount",
            "paid_amount",
            "remaining_amount",
            "reconciliation_status",
            "has_duplicate"
        ]
    ].to_string(index=False)
)


# ==========================================
# 7. DISPLAY REVIEW DATA
# ==========================================

print("\n===== INVOICE REVIEW =====")

if review_invoices.empty:
    print("No invoice issues found.")
else:
    print(
        review_invoices[
            ["invoice_id", "validation_status", "validation_notes"]
        ].to_string(index=False)
    )


print("\n===== PAYMENT REVIEW =====")

if review_payments.empty:
    print("No payment issues found.")
else:
    print(
        review_payments[
            ["transaction_id", "invoice_id", "validation_status", "validation_notes"]
        ].to_string(index=False)
    )

    # ==========================================
# 8. EXPORT EXCEL REPORT
# ==========================================

report_path = export_reconciliation_report(
    result=result,
    exact_duplicates=exact_duplicates,
    conflicting_duplicates=conflicting_duplicates,
    unmatched_payments=unmatched,
    review_invoices=review_invoices,
    review_payments=review_payments
)

print("\n===== EXCEL EXPORT =====")
print(f"Report generated: {report_path}")