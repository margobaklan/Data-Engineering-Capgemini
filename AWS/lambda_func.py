import boto3
import pandas as pd
import io

def lambda_handler(event, context):
    # Initialize S3 client
    s3 = boto3.client('s3')
    
    # Get the uploaded file details
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    # Read the CSV file from S3
    response = s3.get_object(Bucket=bucket, Key=key)
    data = pd.read_csv(io.BytesIO(response['Body'].read()))
    
    # Data Transformation
    # Filter out rows where price is 0 or negative
    data = data[data['price'] > 0]
    
    # Convert last_review to a valid date format and fill missing values
    data['last_review'] = pd.to_datetime(data['last_review'], errors='coerce')
    earliest_date = data['last_review'].min()
    data['last_review'].fillna(earliest_date, inplace=True)

    # Handle missing values in reviews_per_month by setting them to 0
    data['reviews_per_month'].fillna(0, inplace=True)

    # Drop rows with missing latitude or longitude
    data.dropna(subset=['latitude', 'longitude'], inplace=True)
    
    # Save the transformed data
    transformed_csv = data.to_csv(index=False)
    transformed_key = f'transformed/{key}'
    s3.put_object(Bucket=bucket, Key=transformed_key, Body=transformed_csv)
    
    return {
        'statusCode': 200,
        'body': f'Transformed data saved to {transformed_key}'
    }
