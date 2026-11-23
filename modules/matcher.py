import pandas as pd


def reconcile_payments(
    invoices: pd.DataFrame,
    payments: pd.DataFrame
):
    invoices = invoices.copy()
    payments = payments.copy()

    # Required transaction fields
    transaction_fields = [
        "transaction_id",
        "invoice_id",
        "payment_date",
        "payment_amount",
        "payment_method"
    ]

    # Identify exact duplicate rows
    exact_duplicate_mask = payments.duplicated(
        subset=transaction_fields,
        keep="first"
    )

    exact_duplicates = payments[exact_duplicate_mask].copy()

    unique_payments = payments[
        ~exact_duplicate_mask
    ].copy()

    # Identify conflicting transaction IDs
    conflicting_ids = unique_payments.loc[
        unique_payments.duplicated(
            subset=["transaction_id"],
            keep=False
        ),
        "transaction_id"
    ].unique()

    conflicting_duplicates = unique_payments[
        unique_payments["transaction_id"].isin(conflicting_ids)
    ].copy()

    # Exclude conflicting transactions from calculation
    valid_payments = unique_payments[
        ~unique_payments["transaction_id"].isin(conflicting_ids)
    ].copy()

    # Aggregate valid payments
    payment_summary = (
        valid_payments
        .groupby("invoice_id", as_index=False)
        .agg(
            paid_amount=("payment_amount", "sum"),
            transaction_count=("transaction_id", "count")
        )
    )

    # Merge invoices and payment summary
    result = invoices.merge(
        payment_summary,
        on="invoice_id",
        how="left"
    )

    result["paid_amount"] = result["paid_amount"].fillna(0)

    result["transaction_count"] = (
        result["transaction_count"].fillna(0).astype(int)
    )

    # Calculate outstanding balance
    result["remaining_amount"] = (
        result["total_amount"] - result["paid_amount"]
    )

    # Classify payment status
    def classify(row):

        if row["paid_amount"] == 0:
            return "UNPAID"

        elif row["paid_amount"] < row["total_amount"]:
            return "PARTIAL"

        elif row["paid_amount"] == row["total_amount"]:
            return "MATCHED"

        return "OVERPAID"

    result["reconciliation_status"] = result.apply(
        classify,
        axis=1
    )

    # Mark invoices with duplicate transactions
    duplicate_invoice_ids = set(
        exact_duplicates["invoice_id"].dropna()
    ) | set(
        conflicting_duplicates["invoice_id"].dropna()
    )

    result["has_duplicate"] = (
        result["invoice_id"].isin(duplicate_invoice_ids)
    )

    # Identify unmatched payments
    unmatched_payments = valid_payments[
        ~valid_payments["invoice_id"].isin(
            invoices["invoice_id"]
        )
    ].copy()

    # Return reconciliation results
    return (
        result,
        exact_duplicates,
        conflicting_duplicates,
        unmatched_payments
    )