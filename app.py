import streamlit as st
import pandas as pd

# App Config
st.set_page_config(page_title="Supermarket Sales Prediction", page_icon="🛒", layout="centered")

# Title & Tabs
st.title("🛍️ Supermarket Sales Analytics")
tab1, tab2, tab3 = st.tabs(["📈 Overview", "🔮 Prediction", "📋 Raw Data"])

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("supermarket_sales.csv")
    df['Date'] = pd.to_datetime(df['Date'])  # Convert to datetime
    return df

df = load_data()

# Sidebar Filters
st.sidebar.header("🔎 Filters")
city = st.sidebar.multiselect("Select City", df['City'].unique(), default=df['City'].unique())
gender = st.sidebar.multiselect("Select Gender", df['Gender'].unique(), default=df['Gender'].unique())

filtered_df = df[(df['City'].isin(city)) & (df['Gender'].isin(gender))]

# Preprocessing for charts & prediction
sales_over_time = filtered_df.groupby('Date')['Total'].sum().reset_index()
sales_over_time['Moving_Avg_7'] = sales_over_time['Total'].rolling(window=7).mean()

# --- Tab 1: Overview
with tab1:
    st.subheader("📊 Key Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Sales", f"${filtered_df['Total'].sum():,.2f}")
    col2.metric("Average Rating", f"{filtered_df['Rating'].mean():.2f}")
    col3.metric("Average Gross Income", f"${filtered_df['gross income'].mean():.2f}")

    st.subheader("📈 Total Sales and 7-Day Moving Average")
    st.line_chart(sales_over_time.set_index('Date')[['Total', 'Moving_Avg_7']])

# --- Tab 2: Prediction
with tab2:
    st.subheader("🔮 Predict Sales Using 7-Day Moving Average")
    
    min_date = sales_over_time['Date'].min().date()
    max_date = sales_over_time['Date'].max().date()

    selected_date = st.date_input("📅 Select Start Date", min_value=min_date, max_value=max_date)

    direction = st.radio("🔁 Prediction Direction", ['Forward', 'Backward'])
    num_days = st.slider("📆 Number of Days to Predict", min_value=1, max_value=30, value=7)

    if pd.Timestamp(selected_date) in sales_over_time['Date'].values:
        start_idx = sales_over_time.index[sales_over_time['Date'] == pd.Timestamp(selected_date)][0]

        predictions = []
        prediction_dates = []

        if direction == 'Forward':
            if start_idx >= 6:
                for i in range(num_days):
                    idx = start_idx + i
                    if idx < len(sales_over_time):
                        pred = sales_over_time.at[idx, 'Moving_Avg_7']
                    else:
                        pred = predictions[-1] if predictions else sales_over_time['Moving_Avg_7'].dropna().iloc[-1]
                    predictions.append(pred)
                    prediction_dates.append(pd.Timestamp(selected_date) + pd.Timedelta(days=i))
            else:
                st.warning("⚠️ Please select a start date with at least 7 days of previous data.")
        else:  # Backward
            if start_idx >= num_days:
                for i in range(num_days):
                    idx = start_idx - i
                    pred = sales_over_time.at[idx, 'Moving_Avg_7']
                    predictions.append(pred)
                    prediction_dates.append(pd.Timestamp(selected_date) - pd.Timedelta(days=i))
                # Reverse to maintain chronological order
                predictions.reverse()
                prediction_dates.reverse()
            else:
                st.warning("⚠️ Not enough earlier data to go back by selected number of days.")

        if predictions:
            prediction_df = pd.DataFrame({
                'Date': prediction_dates,
                'Predicted_Sales': predictions
            })
            st.success(f"📈 Predicted Sales ({direction}) from {prediction_dates[0].date()} to {prediction_dates[-1].date()}")
            st.dataframe(prediction_df.set_index('Date'))
            st.line_chart(prediction_df.set_index('Date')['Predicted_Sales'])

    else:
        st.warning("⚠️ Selected date not found in data.")

# --- Tab 3: Raw Data
with tab3:
    st.subheader("📋 Filtered Raw Data")
    st.dataframe(filtered_df)

# import streamlit as st
# import pandas as pd

# # ✅ Set custom app name, icon, layout, etc.
# st.set_page_config(
#     page_title="Supermarket Dashboard",       # Title in browser tab
#     page_icon="🛒",                           # Favicon emoji/icon
#     layout="wide"                             # Optional: wide layout
# )
# # Load data
# df = pd.read_csv("supermarket_sales.csv")
# df['Date'] = pd.to_datetime(df['Date'])

# st.title("📊 Supermarket Sales Dashboard with Prediction")

# # Sidebar filters
# city = st.sidebar.multiselect("Select City", df['City'].unique(), default=df['City'].unique())
# gender = st.sidebar.multiselect("Select Gender", df['Gender'].unique(), default=df['Gender'].unique())

# filtered_df = df[(df['City'].isin(city)) & (df['Gender'].isin(gender))]

# sales_over_time = filtered_df.groupby('Date')['Total'].sum().reset_index()
# sales_over_time['Moving_Avg_7'] = sales_over_time['Total'].rolling(window=7).mean()

# # Create tabs with emoji icons in tab labels
# tab1, tab2, tab3 = st.tabs([
#     "📈 Overview",
#     "🔮 Prediction",
#     "📋 Raw Data"
# ])

# with tab1:
#     st.header("📊 Key Metrics")
#     col1, col2, col3 = st.columns(3)
#     col1.metric("Total Sales", f"${filtered_df['Total'].sum():,.2f}")
#     col2.metric("Average Rating", f"{filtered_df['Rating'].mean():.2f}")
#     col3.metric("Average Gross Income", f"${filtered_df['gross income'].mean():,.2f}")

#     st.header("📅 Sales & 7-Day Moving Average")
#     st.line_chart(sales_over_time.set_index('Date')[['Total', 'Moving_Avg_7']])

# with tab2:
#     st.header("🔮 Predict Next 7 Days Sales")

#     min_date = sales_over_time['Date'].min()
#     max_date = sales_over_time['Date'].max()
#     selected_date = st.date_input(
#         "Select Start Date for Prediction",
#         min_value=min_date,
#         max_value=max_date,
#         value=max_date
#     )

#     if selected_date in sales_over_time['Date'].values:
#         start_idx = sales_over_time.index[sales_over_time['Date'] == pd.Timestamp(selected_date)][0]
#         if start_idx >= 6:
#             predictions = []
#             for day in range(7):
#                 idx = start_idx + day
#                 if idx < len(sales_over_time):
#                     pred = sales_over_time.at[idx, 'Moving_Avg_7']
#                 else:
#                     pred = predictions[-1] if predictions else sales_over_time['Moving_Avg_7'].dropna().iloc[-1]
#                 predictions.append(pred)

#             prediction_dates = pd.date_range(start=selected_date, periods=7)
#             prediction_df = pd.DataFrame({
#                 'Date': prediction_dates,
#                 'Predicted Sales ($)': predictions
#             })

#             st.dataframe(prediction_df.set_index('Date'))
#             st.line_chart(prediction_df.set_index('Date')['Predicted Sales ($)'])
#         else:
#             st.warning("⚠️ Select a date with at least 7 previous days of data.")
#     else:
#         st.warning("⚠️ Selected date not found in data.")

# with tab3:
#     st.header("📋 Filtered Raw Data")
#     st.dataframe(filtered_df.reset_index(drop=True))

# # import streamlit as st
# # import pandas as pd

# # # Load data
# # df = pd.read_csv("supermarket_sales.csv")

# # st.title("Simple Supermarket Sales Dashboard with Prediction")

# # # Sidebar filters
# # city = st.sidebar.multiselect("Select City", df['City'].unique(), default=df['City'].unique())
# # gender = st.sidebar.multiselect("Select Gender", df['Gender'].unique(), default=df['Gender'].unique())

# # filtered_df = df[(df['City'].isin(city)) & (df['Gender'].isin(gender))]

# # # Convert Date to datetime
# # filtered_df['Date'] = pd.to_datetime(filtered_df['Date'])

# # # Aggregate total sales by date
# # sales_over_time = filtered_df.groupby('Date')['Total'].sum().reset_index()

# # # Calculate moving average (window = 7 days)
# # sales_over_time['Moving_Avg_7'] = sales_over_time['Total'].rolling(window=7).mean()

# # # Display metrics
# # st.header("Key Metrics")
# # st.metric("Total Sales", f"${filtered_df['Total'].sum():,.2f}")
# # st.metric("Average Rating", f"{filtered_df['Rating'].mean():.2f}")
# # st.metric("Average Gross Income", f"${filtered_df['gross income'].mean():.2f}")

# # # Plot original sales and moving average
# # st.header("Total Sales and 7-Day Moving Average")
# # st.line_chart(sales_over_time.set_index('Date')[['Total', 'Moving_Avg_7']])

# # # User selects a date for prediction start
# # min_date = sales_over_time['Date'].min()
# # max_date = sales_over_time['Date'].max()
# # selected_date = st.date_input("Select a start date for prediction (7 days)", min_value=min_date, max_value=max_date)

# # # Find the index of selected date in sales_over_time dataframe
# # if selected_date in sales_over_time['Date'].values:
# #     start_idx = sales_over_time.index[sales_over_time['Date'] == pd.Timestamp(selected_date)][0]
    
# #     # Check if we have enough data after selected_date for 7-day moving average
# #     if start_idx >= 6:  # need at least 7 days before start_idx to calculate moving avg
# #         # Predict next 7 days sales as moving average of previous 7 days (simple moving avg prediction)
# #         predictions = []
# #         for day in range(7):
# #             idx = start_idx + day
# #             if idx < len(sales_over_time):
# #                 # predicted sales = moving avg at this day
# #                 pred = sales_over_time.at[idx, 'Moving_Avg_7']
# #             else:
# #                 # if beyond available data, use last moving avg known
# #                 pred = predictions[-1] if predictions else sales_over_time['Moving_Avg_7'].dropna().iloc[-1]
# #             predictions.append(pred)
        
# #         prediction_dates = pd.date_range(start=selected_date, periods=7)
# #         prediction_df = pd.DataFrame({
# #             'Date': prediction_dates,
# #             'Predicted_Sales': predictions
# #         })
        
# #         st.subheader(f"Predicted Sales for 7 days starting from {selected_date}")
# #         st.dataframe(prediction_df.set_index('Date'))
        
# #         # Plot predicted sales
# #         st.line_chart(prediction_df.set_index('Date')['Predicted_Sales'])
# #     else:
# #         st.warning("Select a date which has at least 7 previous days data for moving average prediction.")
# # else:
# #     st.warning("Selected date not found in data.")
    
# # # Show filtered data if user wants
# # if st.checkbox("Show filtered data"):
# #     st.dataframe(filtered_df)

