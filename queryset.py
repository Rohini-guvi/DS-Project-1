import streamlit as st
import pymysql as db
import pandas as pd

class SQLQuerySet:
    def __init__(self,db_manager):
        self.db=db_manager

    def execute_query(self,query):
        #Execute the query and Display the out table as Dataframe
        curr=self.db.cursor()
        try:
            data=pd.read_sql(query,self.db)
            st.dataframe(data)
        except Exception as e:
            st.error(str(e))
        curr.close()
        return
    
    #Query-1:Customers with High Average Rating
    def query1(self):
        curr=self.db.cursor()
        curr.execute("""SELECT count("Customer_id") FROM CUSTOMER_TABLE WHERE Average_Rating BETWEEN 4.5 and 5;""")
        total=curr.fetchall()
        st.info(f"Total Customer with High Average Rating: {total[0][0]}")
        query="SELECT * FROM CUSTOMER_TABLE WHERE Average_Rating BETWEEN 4.5 and 5;"
        self.execute_query(query)
        return
    
    #Query-2:Customers with Higher Orders
    def query2(self):
        curr=self.db.cursor()
        curr.execute("""SELECT count("Customer_id") FROM CUSTOMER_TABLE WHERE Total_orders>800;""")
        total=curr.fetchall()
        st.info(f"Total Customer with Higher Orders: {total[0][0]}")
        query="SELECT * FROM CUSTOMER_TABLE WHERE Total_orders>800;"
        self.execute_query(query)
        return
    
    #Query-3:Customers with Higher Order Amount using Inner join and Foreign Key of Customer and Order Tables
    def query3(self):
        query="""SELECT CUSTOMER_TABLE.Customer_id as "Customer_id",ORDERS_TABLE.Order_id as "Order_id",
        ORDERS_TABLE.Restaurant_id as "Restaurant_id",Name,Email,Mobile_number,
        Location,Total_orders,Average_Rating,ORDERS_TABLE.Status as "Status",
        ORDERS_TABLE.Total_amount as "Total_amount"
        FROM CUSTOMER_TABLE INNER JOIN ORDERS_TABLE
        on CUSTOMER_TABLE.Customer_id = orders_table.Customer_id
        WHERE Total_amount>4500;"""
        self.execute_query(query)
        return
    
    #Query-4:Highly preferred Cuisines of customers
    def query4(self):
        curr=self.db.cursor()
        curr.execute("""SELECT Preferred_Cuisine,count(*)as COUNT FROM CUSTOMER_TABLE group by Preferred_Cuisine
                     order by COUNT DESC
                     limit 1;""")
        dish=curr.fetchall()
        st.info(f"{dish[0][0]} is the Highly preferred cuisine with Total Customers of {dish[0][1]}")
        query=""f"SELECT * FROM CUSTOMER_TABLE where Preferred_Cuisine='{dish[0][0]}';"""
        self.execute_query(query)
        return
    
    #Query-5:List of Premium Customers
    def query5(self):
        curr=self.db.cursor()
        curr.execute("""SELECT count("Customer_id") FROM CUSTOMER_TABLE where Premium='Yes';""")
        total=curr.fetchall()
        st.info(f"Total Premium Customers: {total[0][0]}")
        query="SELECT * FROM CUSTOMER_TABLE where Premium='Yes';"
        self.execute_query(query)
        return
    
    #Query-6:Customers Signed-Up in last 2 years
    def query6(self):
        curr=self.db.cursor()
        curr.execute("""SELECT count("Customer_id") FROM CUSTOMER_TABLE WHERE date_format(str_to_date(Signup_Date,'%d-%m-%Y' ),'%Y') between 2023 and 2024 ;""")
        total=curr.fetchall()
        st.info(f"Total Customers Signed-Up in last 2 years: {total[0][0]}")
        query="""SELECT * from CUSTOMER_TABLE WHERE date_format(str_to_date(Signup_Date,'%d-%m-%Y' ),'%Y') between 2023 and 2024 ;"""
        self.execute_query(query)
        return
    
    #Query-7:Restaurants with Higher Orders
    def query7(self):
        curr=self.db.cursor()
        curr.execute("""SELECT count(Restaurant_id) FROM restaurant_table where Total_orders>800;""")
        total=curr.fetchall()
        st.info(f"Total Customer with Higher Orders: {total[0][0]}")
        query="SELECT * FROM restaurant_table where Total_orders>800;"
        self.execute_query(query)
        return
    
    #Query-8:Restaurants with Higher Rating
    def query8(self):
        curr=self.db.cursor()
        curr.execute("""SELECT count("Restaurant_id") FROM restaurant_table WHERE Rating BETWEEN 4.5 and 5;""")
        total=curr.fetchall()
        st.info(f"Total Customer with High Average Rating: {total[0][0]}")
        query="SELECT * FROM restaurant_table WHERE Rating BETWEEN 4.5 and 5;"
        self.execute_query(query)
        return
    
    #Query-9:Highly preferred Cuisines of Restaurants
    def query9(self):
        curr=self.db.cursor()
        curr.execute("""SELECT Cuisine_type,count(*)as COUNT FROM restaurant_table group by Cuisine_type
                     order by COUNT DESC
                     limit 1;""")
        dish=curr.fetchall()
        st.info(f"{dish[0][0]} is the Highly preferred Cuisine in Restaurants with Total of {dish[0][1]}")
        query=""f"SELECT * FROM restaurant_table where Cuisine_type='{dish[0][0]}';"""
        self.execute_query(query)
        return
    
    #Query-10:List of Active Restaurants
    def query10(self):
        curr=self.db.cursor()
        curr.execute("""SELECT count(Restaurant_id) FROM restaurant_table WHERE IsActive='Yes';""")
        total=curr.fetchall()
        st.info(f"Total Active Restaurants: {total[0][0]}")
        query="SELECT * FROM restaurant_table WHERE IsActive='Yes';"
        self.execute_query(query)
        return
    
    #Query-11:Costumers-Peak ordering times and locations
    def query11(self):
        query="""SELECT customer_table.Customer_id,Name,Email,Mobile_number,Location,
        count(Order_date) as "Frequency of orders made",
        Total_orders FROM customer_table right join orders_table
        ON orders_table.Customer_id = customer_table.Customer_id
        where Total_orders>800
        group by customer_table.Customer_id;"""
        self.execute_query(query)
        return
    
    #Query-12:Restaurants with Lower Feedback Rating
    def query12(self):
        curr=self.db.cursor()
        curr.execute("""SELECT count(Restaurant_id) FROM orders_table where Feedback_rating between 1 and 2;""")
        total=curr.fetchall()
        st.info(f"Total Restaurants with Lower Feedback Rating: {total[0][0]}")
        query="""SELECT * FROM orders_table where Feedback_rating between 1 and 2;"""
        self.execute_query(query)
        return
    
    #Query-13:Restaurants-Peak ordering times and locations
    def query13(self):
        query="""SELECT restaurant_table.Restaurant_id as "Restaurant_id",
        Restaurant_Name,Owner_name,contact_number,Location,
        count(Order_date) as "Frequency of orders received in a year",
        Total_orders FROM restaurant_table right join orders_table
        ON orders_table.Restaurant_id = restaurant_table.Restaurant_id
        where Total_orders>800
        group by restaurant_table.Restaurant_id;"""
        self.execute_query(query)
        return
    
    #Query-14:List of Restaurants with Delayed Deliveries
    def query14(self):
        query="""SELECT  orders_table.Order_id as "Order_id",
        delivery_table.Delivery_person_id as "Delivery_person_id",
        Customer_id,Restaurant_id,Order_date,Status,Feedback_rating,
        delivery_table.Delivery_time_in_min as "Delivery Time",
        delivery_table.Estimated_time_in_min as "Estimated Time"
        FROM orders_table LEFT JOIN delivery_table 
        on orders_table.Order_id = delivery_table.Order_id
        where Delivery_time_in_min>Estimated_time_in_min;"""
        self.execute_query(query)
        return
    
    #Query-15:List of Restaurants with Rejected Deliveries
    def query15(self):
        query="""SELECT  * FROM orders_table where orders_table.Status="Cancelled";"""
        self.execute_query(query)
        return
    
    #Query-16:Orders paid with online Transactions
    def query16(self):
        query="""SELECT * FROM ORDERS_TABLE WHERE Payment_mode not in ('Cash','Debit Card','Credit Card');"""
        self.execute_query(query)
        return
    
    #Query-17:List of Delivery Personnel with High Average Rating
    def query17(self):
        curr=self.db.cursor()
        curr.execute("""SELECT count("Delivery_person_id") FROM DELIVERY_PERSONS_TABLE WHERE Average_Rating BETWEEN 4.5 and 5;""")
        total=curr.fetchall()
        st.info(f"Delivery Personnels with High Average Rating: {total[0][0]}")
        query="SELECT * FROM DELIVERY_PERSONS_TABLE WHERE Average_Rating BETWEEN 4.5 and 5;"
        self.execute_query(query)
        return
        
    #Query-18:List of Delivery to far Distances
    def query18(self):
        query="""SELECT * FROM DELIVERY_TABLE WHERE Distance_in_kms>=10;"""
        self.execute_query(query)
        return
    
    #Query-19:List of Delivery Personnel Charging Higher Delivery Fee
    def query19(self):
        query="""SELECT * FROM DELIVERY_TABLE WHERE Delivery_fee>=70;"""
        self.execute_query(query)
        return
    
    #Query-20:List of Successful Delivery made by Bike
    def query20(self):
        query="""SELECT * FROM DELIVERY_TABLE WHERE 
        Vehicle_type in ('Bike','Rental Bike')
        AND Delivery_status='Delivered';"""
        self.execute_query(query)
        return