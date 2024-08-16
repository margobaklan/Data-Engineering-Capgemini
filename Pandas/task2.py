import pandas as pd

def print_grouped_data(grouped_df, message=""):
    print(message)
    print(grouped_df.head(10))
    # print(grouped_df)

df = pd.read_csv('cleaned_airbnb_data.csv')

# Selecting the first 10 rows and the first 3 columns using .iloc
print("First 10 rows and first 3 columns using .iloc:")
print(df.iloc[:10, :3])

# Selecting the first 10 rows and specific columns using .loc
print("\nSelecting specific rows and columns using .loc:")
print(df.loc[:9, ['neighbourhood_group', 'price', 'minimum_nights']])

# Filtering
filtered_df = df[df['neighbourhood_group'].isin(['Manhattan', 'Brooklyn'])]
filtered_df = filtered_df[(filtered_df['price'] > 100) & (filtered_df['number_of_reviews'] > 10)]
filtered_df = filtered_df[['neighbourhood_group', 'price', 'minimum_nights', 'number_of_reviews', 'price_category', 'availability_365']]

# Group the filtered dataset
grouped_df = filtered_df.groupby(['neighbourhood_group', 'price_category']).agg({
    'price': 'mean',
    'minimum_nights': 'mean',
    'number_of_reviews': 'mean',
    'availability_365': 'mean'
}).rename(columns={'price': 'avg_price', 
                   'minimum_nights': 'avg_minimum_nights', 
                   'number_of_reviews': 'avg_number_of_reviews', 
                   'availability_365': 'avg_availability_365'}).reset_index()

# Sorting
sorted_df = filtered_df.sort_values(by=['price', 'number_of_reviews'], ascending=[False, True])

# Ranking of neighborhoods based on the total number of listings and the average price
neighbourhood_ranking = filtered_df.groupby('neighbourhood_group').agg({
    'price': 'mean',
    'neighbourhood_group': 'count'
}).rename(columns={'price': 'avg_price', 'neighbourhood_group': 'total_listings'}).reset_index()

# Sort based on the total number of listings
neighbourhood_ranking = neighbourhood_ranking.sort_values(by='total_listings', ascending=False)

# Output the results of the aggregations and rankings
print_grouped_data(grouped_df, "\nGrouped data by neighbourhood_group and price_category:")
print_grouped_data(sorted_df, "\nSorted DataFrame by price (desc) and number_of_reviews (asc):")
print_grouped_data(neighbourhood_ranking, "\nNeighbourhood ranking:")

# Save the aggregated data
grouped_df.to_csv('aggregated_airbnb_data.csv', index=False)

