# Cross-Environment Compatible Streamlit Template
# Works in: Localhost, SiS Warehouse, SiS Container, Raw SPCS

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

# ============ PAGE CONFIG ============
st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============ CUSTOM CSS ============
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

[data-testid="stMetric"] {
    background: #f8f9fa;
    padding: 12px;
    border-radius: 8px;
    border: 1px solid #e5e5e5;
}
</style>
""", unsafe_allow_html=True)

# ============ CHART COLORS ============
CHART_COLORS = {
    "primary": "#4A90D9",
    "secondary": "#E57373",
    "success": "#81C784",
    "warning": "#FFB74D",
    "accent": "#9575CD",
}


# ============ DATA ============
@st.cache_data
def generate_sample_data():
    np.random.seed(42)
    
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    monthly_df = pd.DataFrame({
        "month": months,
        "revenue": np.random.randint(40, 100, 12),
    })
    
    categories = ["Web", "Mobile", "API", "Desktop", "Other"]
    category_df = pd.DataFrame({
        "category": categories,
        "count": np.random.randint(100, 500, 5),
    })
    
    table_df = pd.DataFrame({
        "Channel": categories * 4,
        "Sessions": np.random.randint(1000, 10000, 20),
        "Users": np.random.randint(500, 5000, 20),
        "Bounce Rate": np.round(np.random.uniform(0.2, 0.6, 20), 2),
        "Conversion": np.round(np.random.uniform(0.01, 0.08, 20), 3),
        "Revenue": np.random.randint(5000, 50000, 20),
    })
    
    return monthly_df, category_df, table_df


monthly_df, category_df, table_df = generate_sample_data()

# ============ SIDEBAR ============
with st.sidebar:
    st.header("Filters")
    date_range = st.selectbox(
        "Date Range",
        ["Last 7 Days", "Last 30 Days", "Last 90 Days"],
        index=1,
    )
    selected_categories = st.multiselect(
        "Categories",
        options=category_df["category"].tolist(),
        default=category_df["category"].tolist(),
    )

filtered_table = table_df[table_df["Channel"].isin(selected_categories)]

# ============ MAIN CONTENT ============
st.title("📊 Dashboard")

# KPI Metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Revenue", f"${filtered_table['Revenue'].sum():,}", "+12%")
with col2:
    st.metric("Users", f"{filtered_table['Users'].sum():,}", "+5%")
with col3:
    st.metric("Conversion", f"{filtered_table['Conversion'].mean()*100:.2f}%", "-0.5%")
with col4:
    st.metric("Sessions", f"{filtered_table['Sessions'].sum():,}", "+8%")

st.divider()

# Charts
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("Monthly Revenue")
    bar_chart = alt.Chart(monthly_df).mark_bar(
        color=CHART_COLORS["primary"]
    ).encode(
        x=alt.X("month:N", sort=None, title=None),
        y=alt.Y("revenue:Q", title="Revenue ($K)"),
        tooltip=["month", "revenue"],
    ).properties(height=250).interactive()
    st.altair_chart(bar_chart, use_container_width=True)

with chart_col2:
    st.subheader("Category Distribution")
    pie_chart = alt.Chart(category_df).mark_arc(innerRadius=50).encode(
        theta=alt.Theta("count:Q"),
        color=alt.Color("category:N", scale=alt.Scale(
            domain=list(category_df["category"]),
            range=list(CHART_COLORS.values()),
        )),
        tooltip=["category", "count"],
    ).properties(height=250)
    st.altair_chart(pie_chart, use_container_width=True)

# Data Table - Using pandas formatting (NOT column_config)
st.subheader("Detailed Data")
display_df = filtered_table.copy()
display_df["Revenue"] = display_df["Revenue"].apply(lambda x: f"${x:,}")
display_df["Bounce Rate"] = display_df["Bounce Rate"].apply(lambda x: f"{x:.0%}")
display_df["Conversion"] = display_df["Conversion"].apply(lambda x: f"{x:.2%}")

st.dataframe(display_df, use_container_width=True, height=300)

# Download
csv = filtered_table.to_csv(index=False)
st.download_button("📥 Download CSV", csv, "data.csv", "text/csv")
