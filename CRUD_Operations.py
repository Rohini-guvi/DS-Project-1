from CRUDoperations import CRUDOperations
import pymysql as db
import streamlit as st

st.header("Performing CRUD operations")

#Creating DB connection
db_connection = db.connect(
    host = "localhost",
    user = "USER",
    password = "root",
    database = "zomato"
    )


# Initialize CRUD operations
crud_ops = CRUDOperations(db_connection)

operation = st.sidebar.selectbox("Select an Operation",["Create","Read","Update","Alter","Insert","Delete"])

if operation=="Create":
    crud_ops.create_table()
elif operation=="Read":
    crud_ops.read_table()
elif operation=="Update":
    crud_ops.update_table()
elif operation=="Insert":
    crud_ops.insert_table()
elif operation=="Delete":
    crud_ops.delete_table()
else:
    crud_ops.alter_table()