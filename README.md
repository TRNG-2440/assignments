# assignments

Coding challenge assignments and other activities to be completed by associates in Training TRNG-2440

## Instructions

* Create a branch of this repository with your name: git checkout -b "your-name" | i.e. git checkout -b josephhighe
* Review the assignment instructions
* Compose necessary code (python/sql/etc)
* Stage, commit and push your assignment code to your branch on this repo

Command to fetch new assignments: `git checkout main -- path_to_file path_to_second_file`

Configurations for Spark session:
`spark = SparkSession.builder     .appName("ConfigExample")     .master("local[*]")     .config("spark.driver.memory", "2g")     .config("spark.executor.memory", "2g")     .config("spark.sql.shuffle.partitions", "4")     .getOrCreate()`
