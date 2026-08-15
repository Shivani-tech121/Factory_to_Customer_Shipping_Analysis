import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(
    page_title="Shipping Route Efficiency Analysis",
    layout="wide"
)

# Dashboard styling
st.markdown("""
<style>
    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 18px;
        color: #888888;
        margin-bottom: 25px;
    }

    [data-testid="stMetric"] {
        background-color: #1f2937;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #374151;
    }

    [data-testid="stMetricLabel"] {
        font-size: 16px;
    }

    [data-testid="stMetricValue"] {
        font-size: 30px;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

# Load dataset
df = pd.read_csv("data/Nassau Candy Distributor.csv")

# Convert dates
df["Order Date"] = pd.to_datetime(
    df["Order Date"],
    dayfirst=True,
    errors="coerce"
)

df["Ship Date"] = pd.to_datetime(
    df["Ship Date"],
    dayfirst=True,
    errors="coerce"
)

# Calculate shipping lead time
df["Shipping Lead Time"] = (
    df["Ship Date"] - df["Order Date"]
).dt.days

# -----------------------------
# Title
# -----------------------------

st.title("🚚 Factory-to-Customer Shipping Route Efficiency Analysis")
st.subheader("Nassau Candy Distributor")

# -----------------------------
# Sidebar Filters
# -----------------------------

st.sidebar.header("Filters")

regions = st.sidebar.multiselect(
    "Select Region",
    options=sorted(df["Region"].dropna().unique()),
    default=sorted(df["Region"].dropna().unique())
)

ship_modes = st.sidebar.multiselect(
    "Select Ship Mode",
    options=sorted(df["Ship Mode"].dropna().unique()),
    default=sorted(df["Ship Mode"].dropna().unique())
)

# Lead-time threshold
threshold = st.sidebar.slider(
    "Lead-Time Threshold (Days)",
    min_value=1,
    max_value=30,
    value=7
)

# -----------------------------
# Apply Filters
# -----------------------------

filtered_df = df[
    (df["Region"].isin(regions)) &
    (df["Ship Mode"].isin(ship_modes))
].copy()

if filtered_df.empty:
    st.warning("No data available for the selected filters. Please select at least one Region and Ship Mode.")
    st.stop()


# -----------------------------
# KPI Calculations
# -----------------------------

total_shipments = len(filtered_df)

average_lead_time = filtered_df[
    "Shipping Lead Time"
].mean()

route_volume = filtered_df[
    ["Region", "State/Province"]
].drop_duplicates().shape[0]

delay_frequency = (
    (filtered_df["Shipping Lead Time"] > threshold).mean() * 100
)

# -----------------------------
# KPI Cards
# -----------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Shipments",
    f"{total_shipments:,}"
)

col2.metric(
    "Average Lead Time",
    f"{average_lead_time:.1f} days"
)

col3.metric(
    "Routes",
    route_volume
)

col4.metric(
    "Delay Frequency",
    f"{delay_frequency:.1f}%"
)

st.divider()

# -----------------------------
# Route Analysis
# -----------------------------

st.header("Route Efficiency Overview")

route_analysis = (
    filtered_df
    .groupby(["Region", "State/Province", "Ship Mode"])
    .agg(
        Total_Shipments=("Order ID", "count"),
        Average_Lead_Time=("Shipping Lead Time", "mean")
    )
    .reset_index()
)

route_analysis["Route"] = (
    route_analysis["Region"] + " - " +
    route_analysis["State/Province"] + " - " +
    route_analysis["Ship Mode"]
)

# -----------------------------
# Top and Bottom Routes
# -----------------------------

col1, col2 = st.columns(2)

with col1:

    st.subheader("Top 10 Efficient Routes")

    top_routes = route_analysis.sort_values(
        "Average_Lead_Time"
    ).head(10)

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.barh(
        top_routes["Route"],
        top_routes["Average_Lead_Time"]
    )

    ax.set_xlabel("Average Lead Time (Days)")
    ax.set_title("Top 10 Efficient Routes")

    ax.invert_yaxis()

    plt.tight_layout()

    st.pyplot(fig)

with col2:

    st.subheader("Bottom 10 Inefficient Routes")

    bottom_routes = route_analysis.sort_values(
        "Average_Lead_Time",
        ascending=False
    ).head(10)

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.barh(
        bottom_routes["Route"],
        bottom_routes["Average_Lead_Time"]
    )

    ax.set_xlabel("Average Lead Time (Days)")
    ax.set_title("Bottom 10 Inefficient Routes")

    ax.invert_yaxis()

    plt.tight_layout()

    st.pyplot(fig)

# -----------------------------
# Ship Mode Analysis
# -----------------------------

st.divider()

st.header("Ship Mode Comparison")

ship_mode_analysis = (
    filtered_df
    .groupby("Ship Mode")
    .agg(
        Total_Shipments=("Order ID", "count"),
        Average_Lead_Time=("Shipping Lead Time", "mean")
    )
    .reset_index()
)

fig, ax = plt.subplots(figsize=(9, 5))

ax.bar(
    ship_mode_analysis["Ship Mode"],
    ship_mode_analysis["Average_Lead_Time"]
)

ax.set_xlabel("Ship Mode")
ax.set_ylabel("Average Lead Time (Days)")
ax.set_title("Average Shipping Lead Time by Ship Mode")

plt.xticks(rotation=30)
plt.tight_layout()

st.pyplot(fig)

# -----------------------------
# Regional Analysis
# -----------------------------

st.divider()

st.header("Geographic Bottleneck Analysis")

region_analysis = (
    filtered_df
    .groupby("Region")
    .agg(
        Total_Shipments=("Order ID", "count"),
        Average_Lead_Time=("Shipping Lead Time", "mean")
    )
    .reset_index()
)

fig, ax = plt.subplots(figsize=(9, 5))

ax.bar(
    region_analysis["Region"],
    region_analysis["Average_Lead_Time"]
)

ax.set_xlabel("Region")
ax.set_ylabel("Average Lead Time (Days)")
ax.set_title("Average Shipping Lead Time by Region")

plt.xticks(rotation=30)
plt.tight_layout()

st.pyplot(fig)

# -----------------------------
# Route Drill-Down
# -----------------------------

st.divider()

st.header("Route Drill-Down")

route_options = sorted(
    route_analysis["Route"].unique()
)

selected_route = st.selectbox(
    "Select a Route",
    route_options
)

selected_data = route_analysis[
    route_analysis["Route"] == selected_route
]

st.dataframe(
    selected_data,
    use_container_width=True
)

# -----------------------------
# Conclusion
# -----------------------------

st.divider()

st.header("Business Insight")

st.write(
    """
    This dashboard analyzes factory-to-customer shipping performance
    using shipping lead time, route volume, geographic performance,
    and shipping mode. It helps identify efficient routes,
    inefficient routes, and potential geographic bottlenecks that
    can support logistics optimization and better delivery planning.
    """
)