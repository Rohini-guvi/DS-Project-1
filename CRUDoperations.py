import streamlit as st
import pymysql as db
import pandas as pd

class CRUDOperations:
    def __init__(self,db_manager):
        self.db=db_manager

    def fetch_tables(self):
        #Fetching Tables from Database
        curr=self.db.cursor()
        curr.execute("""SELECT TABLE_NAME FROM information_schema.tables WHERE TABLE_SCHEMA="zomato";""")
        db_tables=curr.fetchall()
        table=[]
        for i in db_tables:
            table.append(i[0])
        curr.close()
        return table
    
    def fetch_columns(self,table_name):
        #Fetching columns of Selected Table from Database
        curr=self.db.cursor()
        sql=""f'select COLUMN_NAME from information_schema.columns where TABLE_SCHEMA="zomato" and TABLE_NAME="{table_name}";'""
        curr.execute(sql)
        db_columns=curr.fetchall()
        columns=[]
        for i in db_columns:
            columns.append(i[0])
        curr.close()
        return columns

    def create_table(self):
        curr=self.db.cursor()
        table_name=st.text_input("Enter Table Name")
        col_defn=st.text_area("Enter column Definitions")

        if st.button("Create Table"):
            if not table_name or not col_defn:
                st.error("Table Name and Column Definitions are required")
                return
            else:
                query=""f'create table {table_name} ({col_defn});'""
                try:
                    curr=self.db.cursor()
                    curr.execute(query)
                    st.success(f"Table {table_name} created successfully")
                except Exception as e:
                    st.error(str(e))
        
        curr.close()

    def read_table(self):
        #Fetching Tables from Database
        curr=self.db.cursor()
        table=self.fetch_tables()

        table_name=st.selectbox("Select a table",table)
        if table_name:
            query=f"select * from {table_name};"
            try:
                data=pd.read_sql(query,self.db)
                st.dataframe(data)
            except Exception as e:
                st.error(str(e))
        curr.close()
    
    def update_table(self):
        #Fetching Tables from Database
        curr=self.db.cursor()
        table=self.fetch_tables()

        table_name=st.selectbox("Select a table",table)
        if table_name:
            #Fetching Column names for selected Table
            columns=self.fetch_columns(table_name)

            column_to_update=st.selectbox("Select the column to update",columns)
            new_value=st.text_input(f"Enter New value for column {column_to_update}")
            column_condition=st.selectbox("Select the column condition",columns)
            value_condition=st.text_input(f"Enter the value condition for {column_condition}")

            if st.button("Update Table"):
                if not new_value or not value_condition:
                    st.error("Both New value and condition value are required")
                    return
                
                else:

                    query = ""f'UPDATE {table_name} SET {column_to_update} =%s WHERE {column_condition} =%s;'""
                    try:
                        curr.execute(query,[new_value,value_condition])
                        self.db.commit()
                        st.success(f"Updated {column_to_update} in {table_name}")
                    except Exception as e:
                        st.error(f"Error in updating table: {str(e)}")

        curr.close()

    def delete_table(self):
        curr=self.db.cursor()
        table=self.fetch_tables()
        table_name=st.selectbox("Select a table",table)
        if table_name:
            delete_action = st.selectbox("Choose an action",["Delete Row","Drop Table"])
            if delete_action=="Delete Row":
                condition_column = st.selectbox("Select the column condition",self.fetch_columns(table_name))
                condition_value = st.text_input(f"Enter the condition value for {condition_column}")
                if st.button("Delete Row"):
                    query=""f"DELETE FROM {table_name} WHERE {condition_column} = %s;"""
                    try:
                        curr.execute(query,[condition_value])
                        st.success("Row(s) are deleted successfully")
                    except Exception as e:
                        st.error(str(e))
            else:
                if st.checkbox(f"Confirm Drop Table {table_name}"):
                    query=f"DROP TABLE {table_name};"
                    try:
                        curr.execute(query)
                        st.success(f"Table {table_name} is successfully dropped")
                    except Exception as e:
                        st.error(str(e))
        curr.close()

    def insert_table(self):
        curr=self.db.cursor()
        table=self.fetch_tables()

        table_name=st.selectbox("Select a table",table)
        if table_name:
            #Fetching Column names for selected Table
            columns=self.fetch_columns(table_name)

            column_name=st.selectbox("Enter the column name for which the value needs to be inserted",columns)
            value_added=st.text_input(f"Enter the value for {column_name}")
            
            if st.button("Insert Table"):
                if not column_name or not value_added:
                    st.error("Both Column names and values are required")
                    return
                else:
                    query=""f'INSERT INTO {table_name} ({column_name}) VALUES (%s);'""
                    try:
                        curr.execute(query,[value_added])
                        self.db.commit()
                        st.success(f"Value is Inserted successfully to column {column_name}")
                    except Exception as e:
                        st.error(str(e))

        curr.close()

    def alter_table(self):
        curr=self.db.cursor()
        table=self.fetch_tables()
        table_name=st.selectbox("Select a table",table)
        if table_name:
            
            alter_action = st.selectbox("Choose an action",["Add Column","Drop Column","Change Column Name"])
            if alter_action=="Add Column":
                column_name = st.text_input("Enter New column name to be added")
                datatype = st.text_input(f"Enter Datatype for the new column {column_name}")
                if st.button("Add Column"):
                    if column_name and datatype:
                        query=f"ALTER TABLE {table_name} ADD {column_name} {datatype};"
                        try:
                            curr.execute(query)
                            st.success(f"Added new column {column_name} successfully to table {table_name}")
                        except Exception as e:
                            st.error(str(e))
                    
            elif alter_action=="Drop Column":
                drop_column = st.selectbox(f"Select the column to be dropped from table {table_name}",self.fetch_columns(table_name))
                if st.button("Drop Column"):
                    query=f"ALTER TABLE {table_name} DROP COLUMN {drop_column};"
                    try:
                        curr.execute(query)
                        st.success(f"Column {drop_column} is successfully dropped from table {table_name}")
                    except Exception as e:
                        st.error(str(e))
            else:
                change_col_name=st.selectbox(f"Select the column for which column name to be changed in table {table_name}",self.fetch_columns(table_name))
                new_col_name = st.text_input(f"Enter New column name for column {change_col_name}")
                datatype = st.text_input(f"Enter Datatype for the column {change_col_name}")
                if st.button("Change Column Name"):
                    if new_col_name and datatype:
                        query=f"ALTER TABLE {table_name} CHANGE {change_col_name} {new_col_name} {datatype};"
                        try:
                            curr.execute(query)
                            st.success(f"Changed column name {change_col_name} to {new_col_name} successfully in table {table_name}")
                        except Exception as e:
                            st.error(str(e))
                
        curr.close()
