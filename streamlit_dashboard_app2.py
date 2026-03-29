import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

st.set_page_config(page_title="Apple Global Sales Dashboard", layout="wide")
sns.set_style("whitegrid")

@st.cache_data
def load_data():
    df_raw = pd.read_csv("apple_global_sales_dataset.csv")

    df = df_raw.copy()
    df["sale_date"] = pd.to_datetime(df["sale_date"], errors="coerce")
    df["storage"] = df["storage"].fillna("Unknown")
    df["previous_device_os"] = df["previous_device_os"].fillna("Unknown")
    df["customer_rating"] = df["customer_rating"].fillna(df["customer_rating"].median())
    df = df.drop_duplicates()

    df["sale_year"] = df["sale_date"].dt.year
    df["sale_month"] = df["sale_date"].dt.month
    df["sale_day"] = df["sale_date"].dt.day
    df["sale_dayofweek"] = df["sale_date"].dt.dayofweek

    return df_raw, df

df_raw, df = load_data()

st.title("📊 Apple Global Sales Dashboard")
st.caption("Interactive dashboard for exploring sales, revenue, customer ratings, and return behavior.")

st.sidebar.header("Dashboard Filters")

categories = sorted(df["category"].dropna().unique())
channels = sorted(df["sales_channel"].dropna().unique())
countries = sorted(df["country"].dropna().unique())

selected_categories = st.sidebar.multiselect("Category", categories, default=categories)
selected_channels = st.sidebar.multiselect("Sales Channel", channels, default=channels)
selected_countries = st.sidebar.multiselect("Country", countries, default=countries)

year_min = int(df["sale_year"].min())
year_max = int(df["sale_year"].max())
selected_years = st.sidebar.slider("Sale Year Range", year_min, year_max, (year_min, year_max))

filtered_df = df[
    (df["category"].isin(selected_categories)) &
    (df["sales_channel"].isin(selected_channels)) &
    (df["country"].isin(selected_countries)) &
    (df["sale_year"].between(selected_years[0], selected_years[1]))
].copy()

if filtered_df.empty:
    st.warning("No data matches the selected filters.")
    st.stop()

total_revenue = filtered_df["revenue_usd"].sum()
total_units = filtered_df["units_sold"].sum()
avg_rating = filtered_df["customer_rating"].mean()
return_rate = (filtered_df["return_status"].isin(["Returned", "Exchanged"]).mean()) * 100

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Revenue", f"${total_revenue:,.0f}")
c2.metric("Units Sold", f"{total_units:,.0f}")
c3.metric("Average Rating", f"{avg_rating:.2f}")
c4.metric("Return / Exchange Rate", f"{return_rate:.1f}%")

st.markdown("---")

with st.expander("Dataset Overview and Cleaning Summary"):
    col_a, col_b = st.columns(2)

    with col_a:
        st.write("### Raw Data Preview")
        st.dataframe(df_raw.head())

    with col_b:
        st.write("### Filtered Cleaned Data Preview")
        st.dataframe(filtered_df.head())

    st.write("### Cleaning Steps Applied")
    st.markdown(
        """
        - Converted `sale_date` to datetime  
        - Filled missing values in `storage` with `Unknown`  
        - Filled missing values in `previous_device_os` with `Unknown`  
        - Filled missing values in `customer_rating` with the median  
        - Removed duplicate rows  
        - Created date-based features: `sale_year`, `sale_month`, `sale_day`, `sale_dayofweek`
        """
    )

col1, col2 = st.columns(2)

with col1:
    st.subheader("Return Status Distribution")
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.countplot(x="return_status", data=filtered_df, ax=ax)
    ax.set_xlabel("Return Status")
    ax.set_ylabel("Count")
    st.pyplot(fig)
    plt.close(fig)

with col2:
    st.subheader("Revenue by Product Category")
    category_revenue = filtered_df.groupby("category")["revenue_usd"].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(x=category_revenue.index, y=category_revenue.values, ax=ax)
    ax.set_xlabel("Category")
    ax.set_ylabel("Revenue (USD)")
    ax.tick_params(axis="x", rotation=45)
    st.pyplot(fig)
    plt.close(fig)

col3, col4 = st.columns(2)

with col3:
    st.subheader("Top 10 Countries by Revenue")
    top_countries = filtered_df.groupby("country")["revenue_usd"].sum().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(x=top_countries.index, y=top_countries.values, ax=ax)
    ax.set_xlabel("Country")
    ax.set_ylabel("Revenue (USD)")
    ax.tick_params(axis="x", rotation=45)
    st.pyplot(fig)
    plt.close(fig)

with col4:
    st.subheader("Units Sold by Sales Channel")
    channel_units = filtered_df.groupby("sales_channel")["units_sold"].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(x=channel_units.index, y=channel_units.values, ax=ax)
    ax.set_xlabel("Sales Channel")
    ax.set_ylabel("Units Sold")
    ax.tick_params(axis="x", rotation=45)
    st.pyplot(fig)
    plt.close(fig)

col5, col6 = st.columns(2)

with col5:
    st.subheader("Average Customer Rating by Category")
    rating_by_category = filtered_df.groupby("category")["customer_rating"].mean().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(x=rating_by_category.index, y=rating_by_category.values, ax=ax)
    ax.set_xlabel("Category")
    ax.set_ylabel("Average Rating")
    ax.tick_params(axis="x", rotation=45)
    st.pyplot(fig)
    plt.close(fig)

with col6:
    st.subheader("Return Status by Category")
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.countplot(x="category", hue="return_status", data=filtered_df, ax=ax)
    ax.set_xlabel("Category")
    ax.set_ylabel("Count")
    ax.tick_params(axis="x", rotation=45)
    st.pyplot(fig)
    plt.close(fig)

col7, col8 = st.columns(2)

with col7:
    st.subheader("Correlation Heatmap")
    num_cols = [
        "unit_price_usd",
        "discount_pct",
        "units_sold",
        "discounted_price_usd",
        "revenue_usd",
        "customer_rating",
    ]
    corr = filtered_df[num_cols].corr(numeric_only=True)
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
    st.pyplot(fig)
    plt.close(fig)

with col8:
    st.subheader("Numerical Distribution")
    numeric_feature = st.selectbox(
        "Choose a numerical feature",
        [
            "unit_price_usd",
            "discount_pct",
            "units_sold",
            "discounted_price_usd",
            "revenue_usd",
            "customer_rating",
        ],
    )
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(filtered_df[numeric_feature], bins=25, kde=True, ax=ax)
    ax.set_xlabel(numeric_feature)
    ax.set_ylabel("Frequency")
    st.pyplot(fig)
    plt.close(fig)

st.markdown("---")
st.subheader("Detailed Summary Tables")

tab1, tab2, tab3 = st.tabs(["Category Summary", "Country Summary", "Sales Channel Summary"])

with tab1:
    category_summary = (
        filtered_df.groupby("category")
        .agg(
            total_revenue=("revenue_usd", "sum"),
            total_units=("units_sold", "sum"),
            avg_rating=("customer_rating", "mean"),
        )
        .sort_values("total_revenue", ascending=False)
        .reset_index()
    )
    st.dataframe(category_summary, use_container_width=True)

with tab2:
    country_summary = (
        filtered_df.groupby("country")
        .agg(
            total_revenue=("revenue_usd", "sum"),
            total_units=("units_sold", "sum"),
        )
        .sort_values("total_revenue", ascending=False)
        .reset_index()
    )
    st.dataframe(country_summary, use_container_width=True)

with tab3:
    channel_summary = (
        filtered_df.groupby("sales_channel")
        .agg(
            total_units=("units_sold", "sum"),
            total_revenue=("revenue_usd", "sum"),
        )
        .sort_values("total_units", ascending=False)
        .reset_index()
    )
    st.dataframe(channel_summary, use_container_width=True)

st.success("Dashboard loaded successfully.")
