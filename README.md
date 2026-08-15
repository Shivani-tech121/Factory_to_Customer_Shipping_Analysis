# 🚚 Factory-to-Customer Shipping Route Efficiency Analysis

## 📌 Project Overview

The Factory-to-Customer Shipping Route Efficiency Analysis project is an interactive data analytics dashboard developed using Python, Pandas, Matplotlib, and Streamlit.

The project analyzes shipping performance of the Nassau Candy Distributor dataset to identify efficient and inefficient shipping routes, geographic bottlenecks, shipping-mode performance, and delivery delays.

---

## 🎯 Objectives

- Analyze shipping lead time and delivery performance.
- Identify the top 10 most efficient shipping routes.
- Identify the bottom 10 inefficient shipping routes.
- Compare shipping performance across different shipping modes.
- Analyze regional shipping bottlenecks.
- Calculate key performance indicators (KPIs).
- Provide an interactive route-level drill-down.
- Support logistics optimization and better delivery planning.

---

## 🛠️ Technologies Used

- Python
- Pandas
- Matplotlib
- Streamlit

---

## 📊 Dashboard Features

### 1. KPI Dashboard

The dashboard displays:

- Total Shipments
- Average Lead Time
- Number of Routes
- Delay Frequency

### 2. Interactive Filters

Users can filter the dashboard using:

- Region
- Ship Mode
- Lead-Time Threshold

### 3. Route Efficiency Analysis

The dashboard identifies:

- Top 10 Efficient Routes
- Bottom 10 Inefficient Routes

Routes are evaluated based on average shipping lead time.

### 4. Ship Mode Comparison

The dashboard compares the average shipping lead time across different shipping modes.

### 5. Geographic Bottleneck Analysis

Regional shipping performance is analyzed to identify areas with higher shipping lead times.

### 6. Route Drill-Down

Users can select an individual route and view its shipment information and average lead time.

---

## 📈 Key KPIs

### Total Shipments

Total number of shipments available after applying the selected filters.

### Average Lead Time

Average number of days between the order date and ship date.

### Routes

Number of unique Region–State/Province combinations.

### Delay Frequency

Percentage of shipments whose shipping lead time exceeds the selected threshold.

---

## 📂 Project Structure

```text
Factory_to_Customer_Shipping_Analysis/
│
├── apps/
│   └── streamlit_app.py
│
├── data/
│   └── Nassau Candy Distributor.csv
│
├── outputs/
│   ├── dashboard_screenshot.png
│   ├── top_10_routes.png
│   ├── bottom_10_routes.png
│   ├── ship_mode_analysis.png
│   └── regional_analysis.png
│
├── README.md
└── requirements.txt