# 📊 Apple Global Sales Dashboard

This project presents an **interactive Streamlit dashboard** for Exploratory Data Analysis (EDA) on the Apple Global Sales dataset.

---

## 🚀 Features

- 📈 Interactive dashboard with filters (Category, Country, Sales Channel, Year)
- 📊 KPI cards (Revenue, Units Sold, Rating, Return Rate)
- 📉 Visualizations:
  - Return status distribution
  - Revenue by category
  - Top countries by revenue
  - Sales channel performance
  - Customer rating analysis
  - Correlation heatmap
- 📋 Summary tables for deeper insights

---

## 📁 Project Structure

```
.
├── streamlit_dashboard_app.py
├── apple_global_sales_dataset.csv
├── requirements.txt
├── README.md
```

---

## ⚙️ Installation

Install required packages:

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install streamlit pandas matplotlib seaborn scikit-learn
```

---

## ▶️ Run the App

```bash
streamlit run streamlit_dashboard_app.py
```

Then open in browser:

```
http://localhost:8501
```

---

## 🌍 Deployment (Recommended)

You can deploy this dashboard using **Streamlit Community Cloud**:

1. Upload project to GitHub
2. Go to https://share.streamlit.io/
3. Connect your repo
4. Select `streamlit_dashboard_app.py`
5. Click Deploy

---

## 🧹 Data Cleaning Steps

- Converted `sale_date` to datetime
- Filled missing values:
  - `storage` → "Unknown"
  - `previous_device_os` → "Unknown"
  - `customer_rating` → median
- Removed duplicate rows
- Created new features:
  - `sale_year`, `sale_month`, `sale_day`, `sale_dayofweek`

---

## 🎯 Key Insights

- Most transactions are **Kept**, with fewer returns and exchanges
- Revenue is driven by high-value product categories
- Some countries contribute significantly more to total sales
- Customer ratings are generally high
- Units sold and price strongly influence revenue

---

## 📌 Notes

- Ensure the dataset file is in the same directory as the app
- Uses caching for faster performance

---

## 👨‍💻 Author

Ahmed M  
Computer Science Graduate  
Data Science & AI Enthusiast

Give it a ⭐ on GitHub!
