# Findings

1. Parquet was the smallest file size for both dataframes created for Part 2. For the dataframe with 50k rows, the parquet file was 60% the size of the csv file for the same dataframe and about 40% for the dataframe with 500k rows.
2. The size gap did widen as the rows grew from 50k to 500k. Columnar compression would be better than row text because values in a column can be similar (for example the user column is the same prefix `user_` with different numbers), so it's easier for the a parquet file to compress that than storing each row.
3. The parquet file read the fastest in both cases because of the binary nature of the file type.
4. CSV files are better for smaller datasets, but the change would eventually be made to parquet when the dataset is sufficiently large. In the case where a nice tabular format isn't sufficient, i.e. for structured, hierarchial data, a JSON file would be the best option.
5. Reading files from parquet preserves the date time data type when reading the data into a pandas dataframe. This makes a pipeline easier to create, without the need to coerce the data type of any columns which also minimizes the potential for errors when performing that coercion from a CSV file.
