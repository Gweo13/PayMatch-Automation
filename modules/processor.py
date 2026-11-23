import pandas as pd


INVOICE_REQUIRED_COLUMNS = [
    "invoice_id",
    "student_name",
    "program",
    "invoice_date",
    "due_date",
    "total_amount"
]

PAYMENT_REQUIRED_COLUMNS = [
    "transaction_id",
    "invoice_id",
    "payment_date",
    "payment_amount",
    "payment_method"
]


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize column names and text values."""

    df = df.copy()

    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.lower()
        .str.replace(r"\s+", "_", regex=True)
    )

    for column in df.select_dtypes(
        include=["object", "string"]
    ).columns:
        df[column] = df[column].astype("string").str.strip()

    return df


def validate_columns(df: pd.DataFrame, required_columns: list):
    """Check whether all required columns exist."""

    missing = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing required columns: {', '.join(missing)}"
        )


def clean_invoices(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and validate invoice data."""

    df = normalize_columns(df)
    validate_columns(df, INVOICE_REQUIRED_COLUMNS)

    df["invoice_id"] = df["invoice_id"].str.upper()

    df["invoice_date"] = pd.to_datetime(
        df["invoice_date"], errors="coerce"
    )
    df["due_date"] = pd.to_datetime(
        df["due_date"], errors="coerce"
    )
    df["total_amount"] = pd.to_numeric(
        df["total_amount"], errors="coerce"
    )

    df["validation_notes"] = ""

    checks = {
        "invoice_id": df["invoice_id"].isna() | df["invoice_id"].eq(""),
        "student_name": df["student_name"].isna() | df["student_name"].eq(""),
        "program": df["program"].isna() | df["program"].eq(""),
        "invoice_date": df["invoice_date"].isna(),
        "due_date": df["due_date"].isna(),
        "total_amount": df["total_amount"].isna() | (df["total_amount"] <= 0)
    }

    messages = {
        "invoice_id": "Invoice ID kosong",
        "student_name": "Nama siswa kosong",
        "program": "Program kosong",
        "invoice_date": "Tanggal invoice tidak valid",
        "due_date": "Tanggal jatuh tempo tidak valid",
        "total_amount": "Nominal invoice tidak valid"
    }

    for column, invalid in checks.items():
        df.loc[invalid, "validation_notes"] += messages[column] + "; "

    duplicate_mask = (
        df["invoice_id"].notna()
        & df["invoice_id"].ne("")
        & df["invoice_id"].duplicated(keep=False)
    )

    df.loc[duplicate_mask, "validation_notes"] += "Invoice ID duplikat; "

    df["validation_status"] = (
        df["validation_notes"]
        .eq("")
        .map({True: "VALID", False: "REVIEW"})
    )

    return df


def clean_payments(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and validate payment transaction data."""

    df = normalize_columns(df)
    validate_columns(df, PAYMENT_REQUIRED_COLUMNS)

    df["transaction_id"] = df["transaction_id"].str.upper()
    df["invoice_id"] = df["invoice_id"].str.upper()

    df["payment_date"] = pd.to_datetime(
        df["payment_date"], errors="coerce"
    )
    df["payment_amount"] = pd.to_numeric(
        df["payment_amount"], errors="coerce"
    )

    df["validation_notes"] = ""

    checks = {
        "transaction_id": df["transaction_id"].isna() | df["transaction_id"].eq(""),
        "invoice_id": df["invoice_id"].isna() | df["invoice_id"].eq(""),
        "payment_date": df["payment_date"].isna(),
        "payment_amount": df["payment_amount"].isna() | (df["payment_amount"] <= 0),
        "payment_method": df["payment_method"].isna() | df["payment_method"].eq("")
    }

    messages = {
        "transaction_id": "Transaction ID kosong",
        "invoice_id": "Invoice ID kosong",
        "payment_date": "Tanggal pembayaran tidak valid",
        "payment_amount": "Nominal pembayaran tidak valid",
        "payment_method": "Metode pembayaran kosong"
    }

    for column, invalid in checks.items():
        df.loc[invalid, "validation_notes"] += messages[column] + "; "

    df["validation_status"] = (
        df["validation_notes"]
        .eq("")
        .map({True: "VALID", False: "REVIEW"})
    )

    return df