# BigQuery

## Ingesting New Dataset
> Recommend to upload dataset manually or input data to BigQuery directly.
> If you use linking option such as Drive URL, Google Cloud Storage, Amazon S3, Azure Blob Storage, 
> Data Consistency or performance problems probably occur.

### From CSV file
**Source:**
- Create table from: **Upload**
- Select file: `select the file you downloaded locally earlier`
- File format: **CSV**

**Destination:**
- Table name: <name_which_I_want>

**Schema:**
- Check **Auto Detect** for Schema

**Default Rounding Mode**
- **ROUND HALF EVEN (Bankers' Rounding)**:
    - Rounds to the nearest even number when the value is exactly halfway between two numbers.
    - Reduces rounding bias over a large dataset.
- **ROUND HALF ZERO**:
    - Rounds towards zero when the value is exactly halfway.
    - Positive numbers round down, and negative numbers round up to the nearest integer.

### From Google Cloud Storage 
**Source:**
- Create table from: **Google Cloud Storage**
- Select file from GCS bucket: **data-insights-course/exports/products.csv**
- File format: **CSV**

**Destination:**
- Table name: **products**

**Schema:**
- Check **Auto Detect** for Schema.

### From Google Sheets
**Source:**
- Create table from: **Drive**
- Select Drive URI: `put-your-spreadsheet-url-here`
- File format: **Google Sheet**

**Destination:**
- Table type: Leave as default (External table)
- Table name: `<table_name>`

**Schema:**
- Check **Auto Detect** for Schema.

**Advanced options:**
- Set **Header rows to skip:** to **1**.


```sql
SELECT
  *
FROM
  ecommerce.products -- <dataset_name>.<table_name>
ORDER BY
  stockLevel DESC
LIMIT  5

SELECT * FROM ecommerce.products_comments WHERE comments IS NOT NULL
```

```sql
SELECT
  *,
  SAFE_DIVIDE(orderedQuantity,stockLevel) AS ratio
FROM
  ecommerce.products
WHERE
-- include products that have been ordered and are 80% through their inventory
orderedQuantity > 0
AND SAFE_DIVIDE(orderedQuantity,stockLevel) >= .8
ORDER BY
  restockingLeadTime DESC
```

# BigQuery ML

Enabling users to create and execute machine learning models in BigQuery using SQL queries. The goal is to democratise machine learning by enabling SQL practitioners to build models using their existing tools and to increase development speed by eliminating the need for data movement.

1. Create Dataset in BigQuery Studio
2. Create a Model with BigQuery ML SQL
```sql
CREATE OR REPLACE MODEL `bqml_lab.sample_model`
OPTIONS(model_type='logistic_reg') AS
SELECT
  IF(totals.transactions IS NULL, 0, 1) AS label,
  IFNULL(device.operatingSystem, "") AS os,
  device.isMobile AS is_mobile,
  IFNULL(geoNetwork.country, "") AS country,
  IFNULL(totals.pageviews, 0) AS pageviews
FROM
  `bigquery-public-data.google_analytics_sample.ga_sessions_*`
WHERE
  _TABLE_SUFFIX BETWEEN '20160801' AND '20170631'
LIMIT 100000;
```

3. Evaluate the model - [detail](https://developers.google.com/machine-learning/glossary/)
   - linear regression model
     - `mean_absolute_error`, `mean_squared_error`, `mean_squared_log_error`
     - `median_absolute_error`, `r2_score`, `explained_variance`
   - logistic regression model
     - `precision`, `recall`
     - `accuracy`, `f1_score`
     - `log_loss`, `roc_auc`
```sql
SELECT
  *
FROM
  ml.EVALUATE(MODEL `bqml_lab.sample_model`, (
SELECT
  IF(totals.transactions IS NULL, 0, 1) AS label,
  IFNULL(device.operatingSystem, "") AS os,
  device.isMobile AS is_mobile,
  IFNULL(geoNetwork.country, "") AS country,
  IFNULL(totals.pageviews, 0) AS pageviews
FROM
  `bigquery-public-data.google_analytics_sample.ga_sessions_*`
WHERE
  _TABLE_SUFFIX BETWEEN '20170701' AND '20170801'));
```

4. Use the model to predict - defining predicted parameter as `predicted_{feature_name}`

predicting purchase per country
```sql
SELECT
  country,
  SUM(predicted_label) as total_predicted_purchases
FROM
  ml.PREDICT(MODEL `bqml_lab.sample_model`, (
SELECT
  IFNULL(device.operatingSystem, "") AS os,
  device.isMobile AS is_mobile,
  IFNULL(totals.pageviews, 0) AS pageviews,
  IFNULL(geoNetwork.country, "") AS country
FROM
  `bigquery-public-data.google_analytics_sample.ga_sessions_*`
WHERE
  _TABLE_SUFFIX BETWEEN '20170701' AND '20170801'))
GROUP BY country
ORDER BY total_predicted_purchases DESC
LIMIT 10;
```

predicition purchase per user
```sql
SELECT
  fullVisitorId,
  SUM(predicted_label) as total_predicted_purchases
FROM
  ml.PREDICT(MODEL `bqml_lab.sample_model`, (
SELECT
  IFNULL(device.operatingSystem, "") AS os,
  device.isMobile AS is_mobile,
  IFNULL(totals.pageviews, 0) AS pageviews,
  IFNULL(geoNetwork.country, "") AS country,
  fullVisitorId
FROM
  `bigquery-public-data.google_analytics_sample.ga_sessions_*`
WHERE
  _TABLE_SUFFIX BETWEEN '20170701' AND '20170801'))
GROUP BY fullVisitorId
ORDER BY total_predicted_purchases DESC
LIMIT 10;
```
