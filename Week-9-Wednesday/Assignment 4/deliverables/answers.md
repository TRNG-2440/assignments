# Answers to Assignment Questions

## Initial Tables

### Phase 1

- The dataset appears to have some trips with pickup timestamps outside of the expected date range, as indicated by the earliest_trip_timestamp being before January 2024. The latest pickup timestamp is on April 1st at 12:34AM but that can reasonably be attributed to a clerical error in the dataset

### Phase 2

- Query 1: total revenue for PULocationID = 1
  - Estimated bytes processed: 145.7MB
  - Actual bytes processed: 147.79MB
  - Result returned: $93323.95
  - Duration: 237ms
  - Slot ms: 432
- Query 2: pickup & dropoff combination with most trips
  - Estimated bytes processed: 145.7MB
  - Actual bytes processed: 147.79MB
  - Result returned: trips from pickup id 237 to dropoff id 236 had the most trips with 64384
  - Duration: 209ms
  - Slot ms: 321ms
- Query 3: average trip distaince in pickup location id 1 for the first week of 2024 (1/1/2024 - 1/7/2024)
  - Estimated bytes processed: 218.7MB
  - Actual bytes processed: 218.69MB
  - Result returned: average trip distaince was 1.14 miles
  - Duration: 421ms
  - Slot ms: 601ms

### Phase 3

tpep_pickup_datetime was chosen as the partitioned field because it's a time-based field which is the subject of most of the queries management reguraly requests. The chosen clustering fields are PULocationID and DOLocationID because they are fields commonly used in the desired business queries and create significant blocks which can cut down on query execution time.

### Phase 4

Optimized table was saved in dataset as `yellow_tripdata_combined_optimized`

### Phase 5

| Test | Q1 bytes processed | Q2 bytes processed | Q3 bytes processed |
| ---- | ------------------ | ------------------ | ------------------ |
| Normal Table | 147.79MB | 147.79MB | 218.69MD |
| Optimized Table | 129.92MB | 145.79MD | 12.24MB |

Investigation questions:

- Pickup timestamp is a strong partition candidate because it's a time-based, high-cardinality column
- Optimal candidates for paritioning columns should have high cardinality, payment type only has a (relatively) small number of values, so the partitions created wouldn't effectively reduce bytes scanned
- During query execution, if the data is parititoned by a date then it narrows the number of rows scanned for the final result
- Location-based clustering can create significant, smaller blocks with date-partitioned data which optimizes the bytes scanned during query execution
- Clustering does usually make queries faster, but isn't necessarily guaranteed
- Clustering definitions are based on hierarchy so the most frequently referenced fields should be first when defining the clustering for data
- Common query patterns determine what fields in data will be frequently referenced. If those referenced columns are used for partitioning and clustering then that optimizes tables and the queries which follow

### Conclusion

From this assignment, it's evident partitioning and clustering are crucial to table optimization and the queries made for regularly expected business results. The results from repeating the same three queries on an unoptimized and optimized table demonstrate how this tactic can generate the same responses to business questions while reducing the number of bytes scanned, which reduces costs, and has the potential to reduce query execution time.
