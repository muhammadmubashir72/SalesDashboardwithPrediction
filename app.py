import streamlit as st
import pandas as pd

# Load data
df = pd.read_csv("supermarket_sales.csv")

st.title("Simple Supermarket Sales Dashboard with Prediction")

# Sidebar filters
city = st.sidebar.multiselect("Select City", df['City'].unique(), default=df['City'].unique())
gender = st.sidebar.multiselect("Select Gender", df['Gender'].unique(), default=df['Gender'].unique())

filtered_df = df[(df['City'].isin(city)) & (df['Gender'].isin(gender))]

# Convert Date to datetime
filtered_df['Date'] = pd.to_datetime(filtered_df['Date'])

# Aggregate total sales by date
sales_over_time = filtered_df.groupby('Date')['Total'].sum().reset_index()

# Calculate moving average (window = 7 days)
sales_over_time['Moving_Avg_7'] = sales_over_time['Total'].rolling(window=7).mean()

# Display metrics
st.header("Key Metrics")
st.metric("Total Sales", f"${filtered_df['Total'].sum():,.2f}")
st.metric("Average Rating", f"{filtered_df['Rating'].mean():.2f}")
st.metric("Average Gross Income", f"${filtered_df['gross income'].mean():.2f}")

# Plot original sales and moving average
st.header("Total Sales and 7-Day Moving Average")
st.line_chart(sales_over_time.set_index('Date')[['Total', 'Moving_Avg_7']])

# User selects a date for prediction start
min_date = sales_over_time['Date'].min()
max_date = sales_over_time['Date'].max()
selected_date = st.date_input("Select a start date for prediction (7 days)", min_value=min_date, max_value=max_date)

# Find the index of selected date in sales_over_time dataframe
if selected_date in sales_over_time['Date'].values:
    start_idx = sales_over_time.index[sales_over_time['Date'] == pd.Timestamp(selected_date)][0]
    
    # Check if we have enough data after selected_date for 7-day moving average
    if start_idx >= 6:  # need at least 7 days before start_idx to calculate moving avg
        # Predict next 7 days sales as moving average of previous 7 days (simple moving avg prediction)
        predictions = []
        for day in range(7):
            idx = start_idx + day
            if idx < len(sales_over_time):
                # predicted sales = moving avg at this day
                pred = sales_over_time.at[idx, 'Moving_Avg_7']
            else:
                # if beyond available data, use last moving avg known
                pred = predictions[-1] if predictions else sales_over_time['Moving_Avg_7'].dropna().iloc[-1]
            predictions.append(pred)
        
        prediction_dates = pd.date_range(start=selected_date, periods=7)
        prediction_df = pd.DataFrame({
            'Date': prediction_dates,
            'Predicted_Sales': predictions
        })
        
        st.subheader(f"Predicted Sales for 7 days starting from {selected_date}")
        st.dataframe(prediction_df.set_index('Date'))
        
        # Plot predicted sales
        st.line_chart(prediction_df.set_index('Date')['Predicted_Sales'])
    else:
        st.warning("Select a date which has at least 7 previous days data for moving average prediction.")
else:
    st.warning("Selected date not found in data.")
    
# Show filtered data if user wants
if st.checkbox("Show filtered data"):
    st.dataframe(filtered_df)

