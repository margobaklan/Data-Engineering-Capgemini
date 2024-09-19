CREATE OR REPLACE STAGE nyc_stage
    URL='s3://< >' -- your bucket name
    FILE_FORMAT = (TYPE = CSV FIELD_OPTIONALLY_ENCLOSED_BY = '"' SKIP_HEADER = 1);

-- Snowpipe to automatically ingest new CSV files into Snowflake
CREATE OR REPLACE PIPE nyc_pipe AUTO_INGEST = TRUE
AS
COPY INTO NYC_AIRBNB_TABLE
FROM @nyc_stage
FILE_FORMAT = (TYPE = 'CSV');

-- Create the Task for daily transformation
CREATE OR REPLACE TASK daily_airbnb_transform_task
  WAREHOUSE = NYC
  SCHEDULE = 'USING CRON 0 0 * * * UTC'  -- Runs daily at midnight UTC
  COMMENT = 'Daily task to transform raw Airbnb data'
AS
  -- Transforming the data
  -- Create a new table for the transformed data
  CREATE OR REPLACE TABLE transformed_airbnb_data AS
  WITH transformed_data AS (
    SELECT
        id,
        name,
        host_id,
        host_name,
        neighbourhood_group,
        neighbourhood,
        latitude,
        longitude,
        room_type,
        price,
        minimum_nights,
        number_of_reviews,
        
        -- Convert last_review to a valid date format and fill missing values with the earliest available date
        COALESCE(TO_DATE(last_review), 
                 (SELECT MIN(TO_DATE(last_review)) FROM NYC_AIRBNB_TABLE WHERE last_review IS NOT NULL)) AS last_review,
                 
        -- Handle missing values in reviews_per_month by setting them to 0
        COALESCE(reviews_per_month, 0) AS reviews_per_month,
        
        calculated_host_listings_count,
        availability_365
        
    FROM NYC_AIRBNB_TABLE

    -- Filter out rows where price is 0 or negative
    WHERE price > 0

    -- Drop rows with missing latitude or longitude
    AND latitude IS NOT NULL
    AND longitude IS NOT NULL
  )
  SELECT * FROM transformed_data;

-- Enable the task
ALTER TASK daily_airbnb_transform_task RESUME;

-- Manually execute the transformation task
EXECUTE TASK daily_airbnb_transform_task;

-- Use a stream to track changes in the raw and transformed tables 
CREATE OR REPLACE STREAM transformed_airbnb_stream
ON TABLE transformed_airbnb_data
SHOW_INITIAL_ROWS = TRUE;


-- Ensure that there are no NULL values in critical columns
WITH data_quality_check AS (
    SELECT
        COUNT(*) AS null_critical_values
    FROM transformed_airbnb_data
    WHERE price IS NULL
    OR minimum_nights IS NULL
    OR availability_365 IS NULL
)
SELECT 
    CASE 
        WHEN null_critical_values = 0 THEN 'PASS'
        ELSE 'FAIL'
    END AS data_quality_status
FROM data_quality_check;

-- Error Handling: restore data from 2 days ago
CREATE OR REPLACE TABLE transformed_airbnb_data AS
SELECT * FROM transformed_airbnb_data AT OFFSET -2;

-- Create a stream to track changes in raw Airbnb data
CREATE OR REPLACE STREAM raw_airbnb_stream
ON TABLE NYC_AIRBNB_TABLE;

-- Query the stream to detect changes
SELECT * FROM raw_airbnb_stream WHERE METADATA$ACTION = 'INSERT';











