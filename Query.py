import streamlit as st
import pymysql as db
from queryset import SQLQuerySet

st.header("Query to get Data Insights")

#Creating DB connection
db_connection = db.connect(
    host = "localhost",
    user = "USER",
    password = "root",
    database = "zomato"
    )


# Initialize CRUD operations
sql_query = SQLQuerySet(db_connection)

operation = st.selectbox("Select a Query",["Customers with High Average Rating",
                                                   "Customers with Higher Orders",
                                                   "Customers with Higher Order Amount",
                                                   "Highly preferred Cuisines of customers",
                                                   "List of Premium Customers",
                                                   "Customers Signed-Up in last 2 years",
                                                   "Restaurants with Higher Orders",
                                                   "Restaurants with Higher Rating",
                                                   "Highly preferred Cuisines of Restaurants",
                                                   "List of Active Restaurants",
                                                   "Costumers-Peak ordering times and locations",
                                                   "Restaurants with Lower Feedback Rating",
                                                   "Restaurants-Peak ordering times and locations",
                                                   "List of Restaurants with Delayed Deliveries",
                                                   "List of Restaurants with Rejected Deliveries",
                                                   "Orders paid with online Transactions",
                                                   "List of Delivery Personnel with High Rating",
                                                   "List of Delivery to far Distances",
                                                   "List of Delivery Personnel Charging Higher Delivery Fee",
                                                   "List of Successful Delivery made by Bike"
                                                   ])

if operation=="Customers with High Average Rating":
    sql_query.query1()
elif operation=="Customers with Higher Orders":
    sql_query.query2()
elif operation=="Customers with Higher Order Amount":
    sql_query.query3()
elif operation=="Highly preferred Cuisines of customers":
    sql_query.query4()
elif operation== "List of Premium Customers":
    sql_query.query5()
elif operation=="Customers Signed-Up in last 2 years":
    sql_query.query6()
elif operation=="Restaurants with Higher Orders":
    sql_query.query7()
elif operation=="Restaurants with Higher Rating":
    sql_query.query8()
elif operation=="Highly preferred Cuisines of Restaurants":
    sql_query.query9()
elif operation=="List of Active Restaurants":
    sql_query.query10()
elif operation=="Costumers-Peak ordering times and locations":
    sql_query.query11()
elif operation=="Restaurants with Lower Feedback Rating":
    sql_query.query12()
elif operation=="Restaurants-Peak ordering times and locations":
    sql_query.query13()
elif operation=="List of Restaurants with Delayed Deliveries":
    sql_query.query14()
elif operation=="List of Restaurants with Rejected Deliveries":
    sql_query.query15()
elif operation=="Orders paid with online Transactions":
    sql_query.query16()
elif operation=="List of Delivery Personnel with High Rating":
    sql_query.query17()
elif operation=="List of Delivery to far Distances":
    sql_query.query18()
elif operation=="List of Delivery Personnel Charging Higher Delivery Fee":
    sql_query.query19()
else:
    sql_query.query20()