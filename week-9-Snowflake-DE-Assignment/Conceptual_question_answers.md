# Task 1 - Environment Setup

> Q. Why is a warehouse required?

1. In Snowflake, a virtual warehouse provides the necessary compute power (CPU, memory, temporary storage) to run queries, load data and perform updates.
2. It separates compute from storage, since queries run independently without taking up storage space.
3. It prevents workload conflicts, since multiple warehouses of different sizes can be configured to handle different workflows. For example, one warehouse can handle heavy daily reports while another handles fast data loading, ensuring teams do not slow each other down

> Q. Why do we separate raw and clean data?

1. Raw data acts as a permanent historical record. If a pipeline breaks or fails, we can re-run it with the raw data.
2. Running complex data cleaning logic on the fly slows down dashboards. Pre-cleaning and storing data separately makes business queries run much faster.
3. When a report looks wrong, you can compare the clean output against the raw input to see where the data changed or broke.

# Task 3: File format

> Q. What file type did you configure?
> CSV

> Q. What delimiter did you use?
> Comma (,)

> Q. How did you handle the header?
> Skipped the header, since header does not exist in the csv file.

> Q. Why is a file format required?
> A file format is required in Snowflake to tell the system how to parse, interpret, and structure incoming or outgoing data files (such as CSV, JSON, or Parquet). Without it, Snowflake cannot identify field delimiters, skip headers, handle compression, or map data correctly.

# Task 4: External Stage

> Q. What is the purpose of a stage?
> A stage is a temporary storage location used to hold data files before loading them into tables or after unloading them.
> Snowflake tables require structured data and cannot read raw files directly from your local computer or external buckets, so stages act as a secure, intermediate bridge for parsing and moving data

> Q. Does the stage actually store data in Snowflake?
> An internal stage stores data files inside your Snowflake account storage, while an external stage only points to a cloud storage bucket outside of Snowflake
