

from pyspark.sql import SparkSession
import os

def main():
    
        #Part A
        #Create a SparkSession named EnergyUtilityAssignment using local[*]. (3)
        #Set the Spark log level to ERROR. (1)
        #Print Spark version, application name, master, default parallelism and CPU count. (4)
        #Stop the SparkSession correctly. (2)


        spark = (
                SparkSession.builder
                .appName("EnergyUtilityAssignment")
                .master("local[*]")
                .getOrCreate()
        )
        sc = spark.sparkContext
        sc.setLogLevel("ERROR")

        print(f"Spark Version: {spark.version}")
        print(f"Application Name {sc.appName}")
        print(f"master: {sc.master}")
        print(f"Default Parallelism: {sc.defaultParallelism}")
        print(f"CPU count: {os.cpu_count()}")
        
        #Part B
        #[95, 240, 180, 410, 525, 160, 305, 275, 80, 620, 390, 145]
        # Print the number of partitions. (3)
        # Use filter() to keep readings greater than or equal to 300 units. (5)
        # Use map() to convert each retained reading into (reading, "PEAK"). (4)
        # Display peak-reading count using count(). (3)
        # Display the first three peak readings using take(3). (3)
        # Explain which operations are transformations and which are actions. (2)  in comments

        rdd_list =  [95, 240, 180, 410, 525, 160, 305, 275, 80, 620, 390, 145]
        ex = sc.parallelize(    #transformation
                rdd_list,
                 2
        )

        print(f"Number of partitions: {ex.getNumPartitions()}")


        #transformations
        peaks = (ex
                   .filter(lambda x: x >= 300)
                   .map(lambda x: (x,"Peak"))
        )
        
        print(f"Peak reading count {peaks.count()}")  #action

        print("Top Three:")
        print(peaks.take(3))  #action




        #Part A
        spark.stop()

if __name__ == "__main__":
        main()








