# Answers to Investigation Questions

1. The purpose of the stream is to ingest data from the GCS bucket in batches as new data is added.
2. Stream doesn't physically copy the whole table, it stores an offset and then uses underlying metadata to compute the change in data when queried.
3. Rerunning the entire table every time can be costly and can accidentally create duplicates if some records have already been added. Uses a stream only captures the changes in the table.
4. When a successful DML operation is consumed, Snowflake will automatically advance the offset from the current version of the table.
5. Let's Snowflake skip the run entirely is data is already present.
6. A file-load task does external ingestion, pulling new csv files from the GCS bucket. While the CDC-processing does the internal transformation.
