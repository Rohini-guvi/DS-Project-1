import pymysql as db
import streamlit as st
from dataset import TableCreation

#Creating DB connection
db_connection = db.connect(
    host = "localhost",
    user = "USER",
    password = "root",
    database = "zomato"
    )

#Creating Tables for Customer,Delivery,Restaurants,Orders
table_create = TableCreation(db_connection)
table_create.Customer_Table()
table_create.Restaurant_table()
table_create.Orders_table()
table_create.Delivery_table()
table_create.Delivery_persons_table()

current_page=st.navigation([st.Page("Home.py"),st.Page("ViewTable.py"),
                            st.Page("CRUD_Operations.py",title="CRUD Operations"),st.Page("Query.py")])

current_page.run()
