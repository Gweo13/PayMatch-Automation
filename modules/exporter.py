import pandas as pd

from pathlib import Path
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def export_reconciliation_report(
    result: pd.DataFrame,
    exact_duplicates: pd.DataFrame,
    conflicting_duplicates: pd.DataFrame,
    unmatched_payments: pd.DataFrame,
    review_invoices: pd.DataFrame,
    review_payments: pd.DataFrame,
    output_path="output/PayMatch_Report.xlsx"
):
    """Generate a formatted Excel reconciliation report."""

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # ==========================================
    # 1. PREPARE SUMMARY
    # ==========================================

    summary = pd.DataFrame([
        ["Total Invoices", len(result)],
        ["Matched", (result["reconciliation_status"] == "MATCHED").sum()],
        ["Partial", (result["reconciliation_status"] == "PARTIAL").sum()],
        ["Unpaid", (result["reconciliation_status"] == "UNPAID").sum()],
        ["Overpaid", (result["reconciliation_status"] == "OVERPAID").sum()],
        ["Total Invoice Amount", result["total_amount"].sum()],
        ["Total Paid Amount", result["paid_amount"].sum()],
        ["Total Outstanding", result["remaining_amount"].clip(lower=0).sum()],
        ["Exact Duplicates", len(exact_duplicates)],
        ["Conflicting Duplicates", len(conflicting_duplicates)],
        ["Unmatched Payments", len(unmatched_payments)],
        ["Invoice Review", len(review_invoices)],
        ["Payment Review", len(review_payments)]
    ], columns=["Metric", "Value"])

    # ==========================================
    # 2. PREPARE DATA REVIEW
    # ==========================================

    invoice_review = review_invoices.copy()
    payment_review = review_payments.copy()

    invoice_review.insert(0, "record_type", "INVOICE")
    payment_review.insert(0, "record_type", "PAYMENT")

    data_review = pd.concat(
        [invoice_review, payment_review],
        ignore_index=True,
        sort=False
    )

    # ==========================================
    # 3. EXPORT WORKSHEETS
    # ==========================================

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:

        summary.to_excel(
            writer,
            sheet_name="Summary",
            index=False
        )

        result.to_excel(
            writer,
            sheet_name="Invoice Details",
            index=False
        )

        exact_duplicates.to_excel(
            writer,
            sheet_name="Exact Duplicates",
            index=False
        )

        conflicting_duplicates.to_excel(
            writer,
            sheet_name="Conflicting Duplicates",
            index=False
        )

        unmatched_payments.to_excel(
            writer,
            sheet_name="Unmatched Payments",
            index=False
        )

        data_review.to_excel(
            writer,
            sheet_name="Data Review",
            index=False
        )

    # ==========================================
    # 4. FORMAT WORKBOOK
    # ==========================================

    workbook = load_workbook(output_path)

    header_fill = PatternFill(
        fill_type="solid",
        fgColor="1F4E78"
    )

    header_font = Font(
        bold=True,
        color="FFFFFF",
        size=11
    )

    header_alignment = Alignment(
        horizontal="center",
        vertical="center"
    )

    thin_border = Border(
        bottom=Side(style="thin", color="D9E2F3")
    )

    currency_columns = [
        "total_amount",
        "paid_amount",
        "remaining_amount",
        "payment_amount"
    ]

    status_colors = {
        "MATCHED": "C6EFCE",
        "PARTIAL": "FFEB9C",
        "UNPAID": "FFC7CE",
        "OVERPAID": "F4CCCC",
        "VALID": "C6EFCE",
        "REVIEW": "FFC7CE"
    }

    for worksheet in workbook.worksheets:

        worksheet.freeze_panes = "A2"
        worksheet.auto_filter.ref = worksheet.dimensions
        worksheet.row_dimensions[1].height = 25

        # Header formatting
        for cell in worksheet[1]:

            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = header_alignment

        # Column formatting
        for column_cells in worksheet.columns:

            column_letter = get_column_letter(
                column_cells[0].column
            )

            max_length = 0

            for cell in column_cells:

                if cell.value is not None:
                    max_length = max(
                        max_length,
                        len(str(cell.value))
                    )

                cell.border = thin_border
                cell.alignment = Alignment(
                    vertical="center"
                )

            worksheet.column_dimensions[column_letter].width = min(
                max(max_length + 3, 14),
                35
            )

        # Currency formatting
        headers = {
            cell.value: cell.column
            for cell in worksheet[1]
        }

        for column_name in currency_columns:

            if column_name in headers:

                column_number = headers[column_name]

                for row in range(2, worksheet.max_row + 1):

                    worksheet.cell(
                        row=row,
                        column=column_number
                    ).number_format = '"Rp" #,##0;[Red]-"Rp" #,##0'

        # Status coloring
        for row in worksheet.iter_rows(min_row=2):

            for cell in row:

                if cell.value in status_colors:

                    cell.fill = PatternFill(
                        fill_type="solid",
                        fgColor=status_colors[cell.value]
                    )

                    cell.font = Font(bold=True)

    # Special formatting for Summary
    summary_sheet = workbook["Summary"]

    summary_sheet.column_dimensions["A"].width = 28
    summary_sheet.column_dimensions["B"].width = 22

    for row in range(2, summary_sheet.max_row + 1):

        metric = summary_sheet.cell(row, 1).value

        if metric in [
            "Total Invoice Amount",
            "Total Paid Amount",
            "Total Outstanding"
        ]:
            summary_sheet.cell(row, 2).number_format = (
                '"Rp" #,##0;[Red]-"Rp" #,##0'
            )

    workbook.save(output_path)

    return output_path

