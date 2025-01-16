import streamlit as st
import pandas as pd

#View existing tables
st.write("View Existing Databases for Customers,Restaurants,Orders,Deliveries and Delivery Persons")

option = st.selectbox(
    "Select the Table to be viewed",
    ("Customer Table","Restaurants Table","Orders Table","Delivery Table","Delivery Persons Table")
)

if option=="Customer Table":
    df=pd.read_csv("Customer_Table.csv")
    st.table(df)
elif option=="Restaurants Table":
    df=pd.read_csv("Restaurants_Table.csv")
    st.table(df)
elif option=="Orders Table":
    df=pd.read_csv("Orders_Table.csv")
    st.table(df)
elif option=="Delivery Table":
    df=pd.read_csv("Delivery_Table.csv")
    st.table(df)
else:
    df=pd.read_csv("Delivery_Persons_Table.csv")
    st.table(df)