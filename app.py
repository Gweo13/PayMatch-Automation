import streamlit as st
import pandas as pd
import plotly.express as px

from pathlib import Path

from modules.processor import clean_invoices, clean_payments
from modules.matcher import reconcile_payments
from modules.exporter import export_reconciliation_report


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="PayMatch | Payment Reconciliation",
    page_icon="💳",
    layout="wide"
)


# ==========================================
# CUSTOM CSS - PAYMATCH
# ==========================================

st.markdown("""
<style>

/* GLOBAL */
.stApp {
    background: #F4F7FC !important;
}

[data-testid="stAppViewContainer"] {
    background: #F4F7FC !important;
}

.block-container {
    max-width: 1450px;
    padding-top: 1.5rem !important;
    padding-bottom: 3rem;
}

/* STREAMLIT TOP BAR */
header[data-testid="stHeader"] {
    background: #F4F7FC !important;
}

[data-testid="stToolbar"] {
    background: transparent !important;
}

/* TYPOGRAPHY */
h1, h2, h3 {
    color: #142D4E !important;
    font-weight: 700 !important;
}

/* PAYMATCH HEADER */
.paymatch-header {
    background: linear-gradient(120deg, #142D4E 0%, #245B91 100%);
    padding: 30px 34px;
    border-radius: 16px;
    margin-bottom: 26px;
    box-shadow: 0 6px 20px rgba(20,45,78,0.12);
}

.paymatch-title {
    color: #FFFFFF !important;
    font-size: 34px;
    font-weight: 800;
    margin-bottom: 5px;
}

.paymatch-subtitle {
    color: #DCEBFA !important;
    font-size: 16px;
}

.paymatch-description {
    color: #C1D5EA !important;
    font-size: 13px;
    margin-top: 12px;
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background: #FFFFFF !important;
    border-right: 1px solid #E5EAF2;
}

[data-testid="stSidebar"] > div:first-child {
    background: #FFFFFF !important;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #142D4E !important;
}
/* SIDEBAR TEXT */
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h3 {
    color: #142D4E !important;
    font-size: 19px !important;
    font-weight: 750 !important;
}

[data-testid="stSidebar"] label {
    color: #334155 !important;
    font-weight: 600 !important;
}

[data-testid="stSidebar"] p {
    color: #52657D !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label {
    color: #334155 !important;
}

/* INPUT FIELDS */
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stDateInput"] input,
[data-testid="stSelectbox"] div[data-baseweb="select"] > div,
[data-testid="stFileUploader"] section {
    background-color: #FFFFFF !important;
    color: #142D4E !important;
    border-color: #D5DFEA !important;
}

/* INPUT PLACEHOLDER */
input::placeholder {
    color: #94A3B8 !important;
}

/* SELECTBOX TEXT */
[data-baseweb="select"] * {
    color: #142D4E !important;
}

/* FILE UPLOADER */
[data-testid="stFileUploader"] {
    background-color: #FFFFFF !important;
    border-radius: 10px;
}

/* TEXT AREA */
[data-testid="stTextArea"] textarea {
    background-color: #FFFFFF !important;
    color: #142D4E !important;
    border-color: #D5DFEA !important;
}

/* DATAFRAME TEXT */
[data-testid="stDataFrame"] {
    background-color: #FFFFFF !important;
    color: #142D4E !important;
}
/* METRIC CARDS */
[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid #E3EAF3;
    padding: 20px 22px;
    border-radius: 14px;
    box-shadow: 0 3px 12px rgba(20,45,78,0.04);
}

[data-testid="stMetricLabel"] {
    color: #64748B !important;
    font-weight: 600 !important;
}

[data-testid="stMetricValue"] {
    color: #142D4E !important;
    font-weight: 750 !important;
}

/* BUTTONS */
.stButton > button,
.stDownloadButton > button {
    border-radius: 9px;
    font-weight: 650;
    border: 1px solid #245B91;
}

/* TABS */
button[data-baseweb="tab"] {
    font-weight: 600;
    color: #64748B;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #245B91;
}

/* DATAFRAME */
[data-testid="stDataFrame"] {
    border: 1px solid #E3EAF3;
    border-radius: 10px;
    overflow: hidden;
}

/* DIVIDER */
hr {
    border-color: #E2E8F0;
}
/* MULTISELECT */
[data-testid="stMultiSelect"] [data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    border-color: #D5DFEA !important;
}

/* SELECTED STATUS TAGS */
[data-testid="stMultiSelect"] [data-baseweb="tag"] {
    background-color: #EAF2FB !important;
    color: #142D4E !important;
    border: 1px solid #D5DFEA !important;
}

/* TAG TEXT */
[data-testid="stMultiSelect"] [data-baseweb="tag"] span {
    color: #142D4E !important;
}

/* DROPDOWN OPTIONS */
[data-testid="stMultiSelect"] [role="option"] {
    color: #142D4E !important;
    background-color: #FFFFFF !important;
}

/* STREAMLIT TABS - FORCE LIGHT THEME */

[data-testid="stTabs"] [role="tablist"] {
    background-color: #FFFFFF !important;
}

/* ALL TAB BUTTONS */
[data-testid="stTabs"] button[role="tab"] {
    background: #FFFFFF !important;
    color: #334155 !important;
    font-weight: 600 !important;
    border-bottom: 2px solid #E2E8F0 !important;
}

/* ALL TEXT INSIDE TAB BUTTONS */
[data-testid="stTabs"] button[role="tab"] * {
    color: #334155 !important;
    -webkit-text-fill-color: #334155 !important;
}

/* SELECTED TAB */
[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
    background: #FFFFFF !important;
    color: #245B91 !important;
    border-bottom: 3px solid #245B91 !important;
}

/* SELECTED TAB TEXT */
[data-testid="stTabs"] button[role="tab"][aria-selected="true"] * {
    color: #245B91 !important;
    -webkit-text-fill-color: #245B91 !important;
    font-weight: 700 !important;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# HEADER
# ==========================================

st.markdown("""
<div class="paymatch-header">
    <div class="paymatch-title">💳 PayMatch</div>
    <div class="paymatch-subtitle">
        Payment Reconciliation Automation
    </div>
    <div class="paymatch-description">
        Automated invoice matching · Payment verification · Exception detection
    </div>
</div>
""", unsafe_allow_html=True)
# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.markdown("""
<div style="
    padding: 12px 4px 20px 4px;
">
    <div style="
        font-size: 22px;
        font-weight: 800;
        color: #142D4E;
    ">
        💳 PayMatch
    </div>
    <div style="
        font-size: 11px;
        color: #64748B;
        letter-spacing: 1px;
        font-weight: 600;
    ">
        RECONCILIATION SYSTEM
    </div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("### ⚙️ Data Configuration")

data_source = st.sidebar.radio(
    "Select Data Source",
    ["Sample Data", "Upload Excel"]
)

st.sidebar.markdown("---")

st.sidebar.markdown("""
<div style="
    background: #F1F6FC;
    padding: 14px;
    border-radius: 10px;
    border-left: 4px solid #245B91;
">
    <div style="
        font-size: 12px;
        font-weight: 700;
        color: #245B91;
        margin-bottom: 6px;
    ">
        ABOUT PAYMATCH
    </div>
    <div style="
        font-size: 12px;
        color: #52657D;
        line-height: 1.6;
    ">
        Automatically validates invoice records,
        matches transactions, and identifies
        payment exceptions.
    </div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("<br>", unsafe_allow_html=True)

st.sidebar.caption(
    "Payment Reconciliation Automation · v1.0"
)

# ==========================================
# LOAD DATA
# ==========================================

invoices_raw = None
payments_raw = None

if data_source == "Sample Data":

    st.sidebar.success("Sample dataset selected.")

    invoices_raw = pd.read_excel(
        "data/invoices.xlsx"
    )

    payments_raw = pd.read_excel(
        "data/payments.xlsx"
    )

else:

    invoice_file = st.sidebar.file_uploader(
        "Upload Invoices",
        type=["xlsx"]
    )

    payment_file = st.sidebar.file_uploader(
        "Upload Payments",
        type=["xlsx"]
    )

    if invoice_file and payment_file:

        invoices_raw = pd.read_excel(invoice_file)
        payments_raw = pd.read_excel(payment_file)

    else:

        st.info(
            "Upload both invoice and payment Excel files "
            "to start reconciliation."
        )

        st.stop()


# ==========================================
# PROCESS DATA
# ==========================================

try:

    invoices = clean_invoices(invoices_raw)
    payments = clean_payments(payments_raw)

    valid_invoices = invoices[
        invoices["validation_status"] == "VALID"
    ].drop(
        columns=["validation_status", "validation_notes"]
    )

    valid_payments = payments[
        payments["validation_status"] == "VALID"
    ].drop(
        columns=["validation_status", "validation_notes"]
    )

    review_invoices = invoices[
        invoices["validation_status"] == "REVIEW"
    ].copy()

    review_payments = payments[
        payments["validation_status"] == "REVIEW"
    ].copy()

    (
        result,
        exact_duplicates,
        conflicting_duplicates,
        unmatched
    ) = reconcile_payments(
        valid_invoices,
        valid_payments
    )

except Exception as error:

    st.error(f"Unable to process data: {error}")
    st.stop()


# ==========================================
# KPI METRICS
# ==========================================

st.subheader("📊 Reconciliation Overview")

total_invoices = len(invoices)

matched = (
    result["reconciliation_status"] == "MATCHED"
).sum()

partial = (
    result["reconciliation_status"] == "PARTIAL"
).sum()

unpaid = (
    result["reconciliation_status"] == "UNPAID"
).sum()

overpaid = (
    result["reconciliation_status"] == "OVERPAID"
).sum()

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total Invoices", total_invoices)
col2.metric("Matched", matched)
col3.metric("Partial", partial)
col4.metric("Unpaid", unpaid)
col5.metric("Overpaid", overpaid)


# ==========================================
# FINANCIAL OVERVIEW
# ==========================================

st.divider()

st.subheader("💰 Payment Overview")

total_amount = result["total_amount"].sum()
total_paid = result["paid_amount"].sum()

total_outstanding = result[
    "remaining_amount"
].clip(lower=0).sum()

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Invoice Amount",
    f"Rp {total_amount:,.0f}"
)

col2.metric(
    "Total Paid Amount",
    f"Rp {total_paid:,.0f}"
)

col3.metric(
    "Outstanding Amount",
    f"Rp {total_outstanding:,.0f}"
)


# ==========================================
# PAYMENT STATUS CHART
# ==========================================

st.divider()

chart_col, exception_col = st.columns([1.5, 1])

with chart_col:

    st.subheader("Payment Status Distribution")

    status_data = (
        result["reconciliation_status"]
        .value_counts()
        .reset_index()
    )

    status_data.columns = ["Status", "Count"]

    fig = px.pie(
        status_data,
        names="Status",
        values="Count",
        hole=0.55,
        color="Status",
        color_discrete_map={
            "MATCHED": "#22C55E",
            "PARTIAL": "#F59E0B",
            "UNPAID": "#EF4444",
            "OVERPAID": "#8B5CF6"
        }
    )

    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(
            color="#142D4E",
            family="Arial"
        ),
        legend=dict(
            font=dict(color="#334155")
        ),
        margin=dict(
            l=20,
            r=20,
            t=30,
            b=20
        )
    )

    fig.update_traces(
        textfont=dict(color="#FFFFFF"),
        marker=dict(
            line=dict(
                color="#FFFFFF",
                width=3
            )
        )
    )
    st.plotly_chart(
    fig,
    use_container_width=True,
    key="payment_status_distribution"
)


# ==========================================
# EXCEPTION MONITORING
# ==========================================

with exception_col:

    st.subheader("Exception Monitoring")

    st.metric(
        "Exact Duplicates",
        len(exact_duplicates)
    )

    st.metric(
        "Conflicting Transactions",
        len(conflicting_duplicates)
    )

    st.metric(
        "Unmatched Payments",
        len(unmatched)
    )

    st.metric(
        "Data Review",
        len(review_invoices) + len(review_payments)
    )


# ==========================================
# INVOICE DETAILS
# ==========================================

st.divider()

st.subheader("📋 Invoice Reconciliation Details")

status_filter = st.multiselect(
    "Filter Payment Status",
    options=[
        "MATCHED",
        "PARTIAL",
        "UNPAID",
        "OVERPAID"
    ],
    default=[
        "MATCHED",
        "PARTIAL",
        "UNPAID",
        "OVERPAID"
    ]
)

filtered_result = result[
    result["reconciliation_status"].isin(status_filter)
]

display_columns = [
    "invoice_id",
    "student_name",
    "program",
    "total_amount",
    "paid_amount",
    "remaining_amount",
    "reconciliation_status",
    "has_duplicate"
]

st.dataframe(
    filtered_result[display_columns],
    use_container_width=True,
    hide_index=True,
    column_config={
        "total_amount": st.column_config.NumberColumn(
            "Invoice Amount",
            format="Rp %d"
        ),
        "paid_amount": st.column_config.NumberColumn(
            "Paid Amount",
            format="Rp %d"
        ),
        "remaining_amount": st.column_config.NumberColumn(
            "Remaining",
            format="Rp %d"
        ),
        "has_duplicate": st.column_config.CheckboxColumn(
            "Duplicate Flag"
        )
    }
)


# ==========================================
# EXCEPTION DETAILS
# ==========================================

st.divider()

st.subheader("🔍 Exception Details")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Exact Duplicates",
    "Conflicting Duplicates",
    "Unmatched Payments",
    "Invoice Review",
    "Payment Review"
])

with tab1:

    st.dataframe(
        exact_duplicates,
        use_container_width=True,
        hide_index=True
    )

with tab2:

    st.dataframe(
        conflicting_duplicates,
        use_container_width=True,
        hide_index=True
    )

with tab3:

    st.dataframe(
        unmatched,
        use_container_width=True,
        hide_index=True
    )

with tab4:

    st.dataframe(
        review_invoices,
        use_container_width=True,
        hide_index=True
    )

with tab5:

    st.dataframe(
        review_payments,
        use_container_width=True,
        hide_index=True
    )


# ==============================
# EXCEL EXPORT
# ==============================

st.subheader("📥 Excel Report")

if st.button("Generate Excel Report", type="primary"):

    report_path = export_reconciliation_report(
        result,
        exact_duplicates,
        conflicting_duplicates,
        unmatched,
        review_invoices,
        review_payments
    )

    st.session_state["report_path"] = report_path
    st.success("Excel report berhasil dibuat!")

# Tampilkan preview jika report sudah dibuat
if "report_path" in st.session_state:

    report_path = st.session_state["report_path"]

    excel_file = pd.ExcelFile(report_path)

    st.markdown("### 📊 Report Preview")

    report_tabs = st.tabs(excel_file.sheet_names)

    for tab, sheet_name in zip(report_tabs, excel_file.sheet_names):

        with tab:
            preview = pd.read_excel(
                report_path,
                sheet_name=sheet_name
            )

            st.dataframe(
                preview,
                use_container_width=True,
                hide_index=True
            )

    with open(report_path, "rb") as file:
        st.download_button(
            label="⬇️ Download Excel Report",
            data=file,
            file_name="PayMatch_Report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "PayMatch | Payment Reconciliation Automation | "
    "Built with Python, Pandas, Streamlit & OpenPyXL"
)