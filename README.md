# DS-Project-1
Zomata - Food Delivery Data Insights Using Python and SQL

**Objective:**

The objective of this project is to analyze Business Use cases like Order Management,Customer Analytics,Delivery Optimization and Restaurant Insights.
This project also gives the overview of Customer preferences and order patterns, peak ordering times and Location, Delivery personnel performance, Highly preferred Restaurants and Cuisines and track Delivery to find the delays.

**Approach:**
- Using Faker Library, created random values and populated in the tables Customer,Delivery Personnel,Delivery, Orders and Restaurants.
- The tables are then stored in the Database MySQL by establishing connections with Database.
- Interactive Streamlit app is created to view the tables and access the data for future analysis.
- CRUD operations can also be performed on those tables.
- 20 SQL queries are created to get insights of the data.

**Code flow:**

Streamlit App Page structure

main.py

|---------------Home.py

|---------------ViewTable.Py

|---------------CRUD_Operations.py

|---------------Query.py

**CRUD Operations done:**
- CREATE
- SELECT
- UPDATE using WHERE condition
- DELETE- Row or Drop Table
- INSERT 
- ALTER – Adding Row, Drop column, Change column name

**Insights:**
- Customers with High Average Rating
- Customers with Higher Orders
- Customers with Higher Order Amount
- Highly preferred Cuisines of customers
- List of Premium Customers
- Customers Signed-Up in last 2 years
- Restaurants with Higher Orders
- Restaurants with Higher Rating
- Highly preferred Cuisines of Restaurants
- List of Active Restaurants
- Costumers-Peak ordering times and locations
- Restaurants with Lower Feedback Rating
- Restaurants-Peak ordering times and locations
- List of Restaurants with Delayed Deliveries
- List of Restaurants with Rejected Deliveries
- Orders paid with online Transactions
- List of Delivery Personnel with High Rating
- List of Delivery to far Distances
- List of Delivery Personnel Charging Higher Delivery Fee
- List of Successful Delivery made by Bike
