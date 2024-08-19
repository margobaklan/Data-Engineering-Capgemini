import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Neighborhood Distribution of Listings
def plot_neighborhood_distribution(df):
    plt.figure(figsize=(10, 6))
    neighborhood_counts = df['neighbourhood_group'].value_counts()
    sns.barplot(x=neighborhood_counts.index, y=neighborhood_counts.values, palette='viridis')
    plt.title('Neighborhood Distribution of Listings')
    plt.xlabel('Neighborhood Group')
    plt.ylabel('Number of Listings')
    for i in range(len(neighborhood_counts)):
        plt.text(i, neighborhood_counts.values[i] + 50, str(neighborhood_counts.values[i]), ha='center')
    plt.savefig('neighborhood_distribution.png')
    plt.show()

# Price Distribution Across Neighborhoods
def plot_price_distribution(df):
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='neighbourhood_group', y='price', data=df, palette='coolwarm')
    plt.title('Price Distribution Across Neighborhoods')
    plt.xlabel('Neighborhood Group')
    plt.ylabel('Price')
    plt.ylim(0, df['price'].quantile(0.95))  
    plt.savefig('price_distribution.png')
    plt.show()

# Room Type vs. Availability
def plot_room_type_availability(df):
    plt.figure(figsize=(10, 6))
    sns.barplot(x='neighbourhood_group', y='availability_365', hue='room_type', data=df, errorbar='sd', palette='Set2')
    plt.title('Room Type vs. Availability Across Neighborhoods')
    plt.xlabel('Neighborhood Group')
    plt.ylabel('Average Availability (365 days)')
    plt.legend(title='Room Type')
    plt.savefig('room_type_availability.png')
    plt.show()

# Correlation Between Price and Number of Reviews
def plot_price_reviews_correlation(df):
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='price', y='number_of_reviews', hue='room_type', data=df, palette='husl', alpha=0.7)
    sns.regplot(x='price', y='number_of_reviews', data=df, scatter=False, color='red')
    plt.title('Correlation Between Price and Number of Reviews')
    plt.xlabel('Price')
    plt.ylabel('Number of Reviews')
    plt.ylim(0, df['number_of_reviews'].quantile(0.95))  
    plt.legend(title='Room Type')
    plt.savefig('price_reviews_correlation.png')
    plt.show()

# Time Series Analysis of Reviews
def plot_review_trends(df):
    plt.figure(figsize=(10, 6))
    df['review_month'] = df['last_review'].dt.to_period('M')
    reviews_over_time = df.groupby(['review_month', 'neighbourhood_group']).agg({'number_of_reviews': 'sum'}).unstack()
    reviews_over_time.rolling(window=3).mean().plot(ax=plt.gca(), marker='o', alpha=0.7)
    plt.title('Time Series Analysis of Reviews')
    plt.xlabel('Month')
    plt.ylabel('Number of Reviews')
    plt.legend(title='Neighborhood Group')
    plt.savefig('review_trends.png')
    plt.show()

# Price and Availability Heatmap
def plot_price_availability_heatmap(df):
    plt.figure(figsize=(10, 6))
    df['price_category'] = pd.qcut(df['price'], q=10, labels=False)
    heatmap_data = df.pivot_table(index='neighbourhood_group', columns='price_category', values='availability_365', aggfunc='mean')
    sns.heatmap(heatmap_data, cmap='coolwarm', annot=True, fmt='.1f')
    plt.title('Price and Availability Heatmap')
    plt.xlabel('Price Category (Deciles)')
    plt.ylabel('Neighborhood Group')
    plt.savefig('price_availability_heatmap.png')
    plt.show()

# Room Type and Review Count Analysis
def plot_room_type_review_count(df):
    plt.figure(figsize=(10, 6))
    review_counts = df.groupby(['neighbourhood_group', 'room_type'])['number_of_reviews'].sum().unstack()
    review_counts.plot(kind='bar', stacked=True, ax=plt.gca(), colormap='tab20c')
    plt.title('Room Type and Review Count Analysis')
    plt.xlabel('Neighborhood Group')
    plt.ylabel('Number of Reviews')
    plt.legend(title='Room Type')
    plt.savefig('room_type_review_count.png')
    plt.show()

df = pd.read_csv('AB_NYC_2019.csv')

df.dropna(subset=['price', 'number_of_reviews', 'availability_365', 'last_review'], inplace=True)
df['last_review'] = pd.to_datetime(df['last_review'])

plot_neighborhood_distribution(df)
plot_price_distribution(df)
plot_room_type_availability(df)
plot_price_reviews_correlation(df)
plot_review_trends(df)
plot_price_availability_heatmap(df)
plot_room_type_review_count(df)