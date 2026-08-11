# Answers to Questions in the Assignment

## Task 1

Used the X-Small warehouse already created in Snowflake, but looked up the steps for creating a X-small warehouse.

1. The warehouse includes the compute resources which will be needed to perform tasks in the assignment.
2. Separating raw and clean data allows us to repeatedly use the raw data in case different business objectives are created later using the same data.

## Task 2

* File name: S3://sfquickstarts/tastybytes/raw_pos/menu/menu.csv.gz
* File type: CSV using GZIP for compression
* Delimiter: comma
* Header exists
* 11 columns total

## Task 3

1. CSV file configuration
2. comma
3.
4. FILE FORMAT tells Snowflake what kind of file to expect from the bytes.

## Task 4

1. The purpose of the stage is to create a connection to the directory of the URL so Snowflake can then access files such as the CSV.
2. No

## Task 5

1. 100 rows loaded
2. 1 file processed
3. 0 errors

## Task 6

1. 58 unique menu items (distinct menu item names)
2. 15 unique truck brands
3. 4 unique categories
4. $2
5. $21
6. $7.18

## Task 7 (no questions to answer)

## Task 8

1. Rack of Pork Ribs, The King Combo, Tandoori Mixed Grill, Tonkatsu Ramen, Creamy Chicken Ramen
2. Spicy Miso Vegetable Ramen, Tonkatsy Ramen, Rack of Pork Ribs, Chicken Burrito, Creamy Chicken Ramen
3. Kitakata Ramen Bar (average sell price of $9.96)
4. Kitakata Ramen Bar (average profit of $6)
5. Snack - 5, Main - 43, Dessert - 6, Beverage - 46
6. Budget - 48, Standard - 18, Premium - 23, Deluxe - 11

## Task 9

Status columns added to clean_menu table

## Task 10

Kitakata Ramen Bar has the highest average profit.
