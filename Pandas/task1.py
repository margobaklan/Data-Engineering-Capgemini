import pandas as pd

def print_dataframe_info(df, message=""):
    print(message)
    print(df.head(10))
    print("\nDataFrame Info:")
    df.info()
    print("\nMissing values per column:")
    print(df.isnull().sum())

# Data Transformation Functions
def categorize_price(price):
    if price < 100:
        return 'Low'
    elif 100 <= price < 300:
        return 'Medium'
    else:
        return 'High'

def categorize_length_of_stay(minimum_nights):
    if minimum_nights <= 3:
        return 'Short-term'
    elif 4 <= minimum_nights <= 14:
        return 'Medium-term'
    else:
        return 'Long-term'

# Data Loading and Initial Inspection
df = pd.read_csv('AB_NYC_2019.csv')

# Output the state of the DataFrame before 
print_dataframe_info(df, "\nDataFrame before cleaning and transformations:")

# Handling Missing Values
df.fillna({'name': "Unknown"}, inplace=True)
df.fillna({'host_name': "Unknown"}, inplace=True)
df.fillna({'last_review': "NaT"}, inplace=True)

# Data Transformation
df['price_category'] = df['price'].apply(categorize_price)
df['length_of_stay_category'] = df['minimum_nights'].apply(categorize_length_of_stay)

# Ensure no missing values in critical columns
assert df['name'].isnull().sum() == 0, "Missing values found in 'name'"
assert df['host_name'].isnull().sum() == 0, "Missing values found in 'host_name'"
assert df['last_review'].isnull().sum() == 0, "Missing values found in 'last_review'"

# Confirm all price values are greater than 0
df = df[df['price'] > 0]

# Output the state of the DataFrame after 
print_dataframe_info(df, "\nDataFrame after cleaning and transformations:")

# Save the cleaned dataset as a new CSV file
df.to_csv('cleaned_airbnb_data.csv', index=False)