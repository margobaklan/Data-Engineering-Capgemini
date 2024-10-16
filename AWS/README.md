# ETL Pipeline for NYC Airbnb Open Data

## 1. Set Up the Environment

To set up the required AWS services, follow these steps:

- **S3 Bucket**: Create an S3 bucket named `nyc-airbnb-data-storage` for storing the dataset.
- **Amazon Redshift**: Create an Amazon Redshift cluster named `nyc-airbnb-redshift` for querying the transformed data.
- **AWS Lambda**: Set up AWS Lambda for data transformation. The code for this can be found in `lambda_func.py`.
- **AWS Step Functions**: Use AWS Step Functions for orchestrating the ETL process.
- **Upload Data**: Upload the NYC Airbnb Open Data CSV file to the S3 bucket created above.

## 2. Data Ingestion

- Set up S3 as the storage for the raw dataset by uploading your CSV file to the `nyc-airbnb-data-storage` bucket.
- Create an S3 event trigger to call the AWS Lambda function whenever new data is uploaded.

## 3. Data Transformation Using AWS Lambda

Data transformation logic is implemented in `lambda_func.py`. This function will process the data as follows:
- Filter out rows where the price is 0 or negative.
- Convert `last_review` to a valid date format, filling missing values with the earliest available date.
- Handle missing values in `reviews_per_month` by setting them to 0.
- Drop rows with missing latitude or longitude.

After transformation, the data should be sent to Amazon Redshift for storage and analysis.

## 4. Create Tables in Amazon Redshift

In Amazon Redshift, create the following tables to store the raw and transformed data:

- **Raw Table**: Stores the original unprocessed data. CREATE TABLE raw_airbnb_data (...)
- **Processed Table**: Stores the cleaned and transformed data. CREATE TABLE processed_airbnb_data (...)

## 5. Data Loading into Redshift
Use the COPY command in Redshift to load the transformed data from S3 into Redshift. Below is an example command:

```sql
COPY processed_airbnb_data
FROM 's3://nyc-airbnb-data-storage/.csv'
IAM_ROLE '...'
CSV;
```

## 6. Data Quality Checks
Implement data quality checks using Redshift SQL to ensure no critical fields contain NULL values.

```sql
SELECT COUNT(*) FROM processed_airbnb_data WHERE price IS NULL;
SELECT COUNT(*) FROM processed_airbnb_data WHERE minimum_nights IS NULL;
SELECT COUNT(*) FROM processed_airbnb_data WHERE availability_365 IS NULL;
```
To validate data consistency after loading:
```sql
SELECT * FROM processed_airbnb_data WHERE price < 0;
SELECT * FROM processed_airbnb_data WHERE minimum_nights < 0;
```

## 7. Real-Time Monitoring and Streaming
- Use AWS Step Functions to orchestrate the pipeline:
- Set up the pipeline to monitor for new data uploads in S3.
- Trigger the Lambda function for data transformation and loading into Redshift.
- Monitor the pipeline using AWS CloudWatch to track execution logs, detect errors, and ensure that the pipeline runs smoothly.

## 8. Automation Using AWS Step Functions
- Use CloudWatch Events to trigger Step Functions at a scheduled interval (e.g., daily or hourly).
- Ensure the entire ETL process, from ingestion to transformation and loading, runs automatically with little manual intervention.
