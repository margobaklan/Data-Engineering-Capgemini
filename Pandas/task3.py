import pandas as pd

def print_analysis_results(result, message=""):
    print(message)
    print(result)

df = pd.read_csv('cleaned_airbnb_data.csv')

# Summary of average prices across neighbourhood_group and room_type
pricing_trends = df.pivot_table(values='price', index='neighbourhood_group', columns='room_type', aggfunc='mean')
print_analysis_results(pricing_trends, "\nPricing Trends Across Neighborhoods and Room Types:")

# Transform the dataset from wide to long format
metrics_long_format = pd.melt(df, id_vars=['neighbourhood_group', 'room_type'], value_vars=['price', 'minimum_nights'])
print_analysis_results(metrics_long_format, "\nData in Long Format:")

# Create availability_status column
def classify_availability(days):
    if days < 50:
        return "Rarely Available"
    elif 50 <= days <= 200:
        return "Occasionally Available"
    else:
        return "Highly Available"

df['availability_status'] = df['availability_365'].apply(classify_availability)

# Analyze trends using availability_status
availability_trends = df.groupby(['availability_status']).agg({
    'price': 'mean',
    'number_of_reviews': 'mean',
    'availability_365': 'mean',
    'neighbourhood_group': 'count'
}).rename(columns={'neighbourhood_group': 'total_listings'})
print_analysis_results(availability_trends, "\nAvailability Trends and Patterns:")

# Basic descriptive statistics
descriptive_stats = df[['price', 'minimum_nights', 'number_of_reviews']].describe()
print_analysis_results(descriptive_stats, "\nDescriptive Statistics:")

# Convert last_review to datetime and set as index
df['last_review'] = pd.to_datetime(df['last_review'])
df.set_index('last_review', inplace=True)
print_analysis_results(df.head(), "\nDataFrame with last_review as datetime index:")

# Resample data to observe monthly trends
monthly_trends = df.resample('ME').agg({
    'price': 'mean',
    'number_of_reviews': 'sum'
})
print_analysis_results(monthly_trends, "\nMonthly Trends in Number of Reviews and Average Prices:")

# Group data by month to analyze seasonal patterns
df['month'] = df.index.month
seasonal_patterns = df.groupby('month').agg({
    'price': 'mean',
    'number_of_reviews': 'sum'
})
print_analysis_results(seasonal_patterns, "\nSeasonal Patterns by Month:")

# Save the results of the time series analysis
monthly_trends.to_csv('time_series_airbnb_data.csv', index=True)




