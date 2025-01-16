from faker import Faker
import pandas as pd
import random
from datetime import datetime, timedelta
import streamlit as st

class TableCreation:
    def __init__(self,db_connection):
        self.NUM_CUSTOMERS =1000
        self.NUM_RESTAURANTS=500
        self.NUM_DELIVERIES=2000
        self.NUM_ORDERS= 1500
        self.NUM_DELIVERY_PERSONS=1000
        
        #Creating DB connection
        self.db_connection = db_connection

    fake = Faker(locale="en_IN")
    def fake_phone_number(self,fake:Faker):
        return f'+91 {fake.msisdn()[3:]}'

    def fake_signupdate(self,fake:Faker):
        date_time=fake.date_this_decade()
        return date_time.strftime('%d-%m-%Y')

    def fake_food_preference(self):
        fav_food=['Pizza','Biryani','Idly','Onion Masala Dosa','Pav Bhaji','Samosa','Chicken Tandoori Shawarma','Chole Bhature','Burger','KFC','Sandwich','Cakes',
                'Pasta','Sweets','Soup','Mutton Fry','Fish Fry','Chicken Fry','Appam','Noodles','Omelette','Coffee','Tea','Poori','Chappathi','Roti']
        return random.choice(fav_food)

    def fake_restaurant_Name(self,fake:Faker):
        return fake.first_name()+" "+random.choice(['Restaurant','Bhojanalya','Unavagam','Bhavan','Hotel','','Sweets','Bakery'])

    def Write_to_CSV(self,out_table,column,file_name):
        db_table = pd.DataFrame(out_table, columns= column)
        db_table.to_csv(file_name,index=False)
        return
    
    #Creating Customer Table on DB
    def Customer_Table(self):
        
        curr = self.db_connection.cursor()
        fake = Faker(locale="en_IN")
        #Query to create table
        table = """
        CREATE TABLE ZOMATO.CUSTOMER_TABLE
        (
        Customer_id INT PRIMARY KEY,
        Name VARCHAR(50),
        Email VARCHAR(100),
        Mobile_number VARCHAR(15),
        Location VARCHAR(100),
        Signup_Date VARCHAR(15),
        Premium VARCHAR(5),
        Preferred_Cuisine VARCHAR(50),
        Total_orders INT,
        Average_Rating FLOAT
        );
        """
        try:
            curr.execute(table)
        
            #Insert values into table using Faker
            rows=[]
            for i in range(1,self.NUM_CUSTOMERS+1):
                a=[i,fake.name(),fake.email(),self.fake_phone_number(fake),fake.address(),
                self.fake_signupdate(fake),random.choice(['Yes','No']),self.fake_food_preference(),
                random.randint(1,1000),round(random.uniform(1,5),1)]
                rows.append(tuple(a))
        
            insert = """
            insert into customer_table
            (Customer_id, Name,Email,Mobile_number,Location,Signup_Date,Premium,Preferred_Cuisine,Total_orders,Average_Rating)
            values
            (%s, %s,%s, %s,%s, %s,%s, %s,%s, %s);
            """
            
            curr.executemany(insert, rows)
            self.db_connection.commit()
            
            #Write the table to CSV
            curr.execute("select * from customer_table")
            out_table=curr.fetchall()
            col = [i[0] for i in curr.description]
            self.Write_to_CSV(out_table,col,"Customer_Table.csv")

        except Exception as e:
            pass
        curr.close()
        
        return
    
    #Creating Restaurants Table on DB
    def Restaurant_table(self):
        curr = self.db_connection.cursor()
        fake = Faker(locale="en_IN")
        #Query to create table
        table = """
        CREATE TABLE ZOMATO.RESTAURANT_TABLE
        (
        Restaurant_id INT PRIMARY KEY,
        Restaurant_Name VARCHAR(50),
        Cuisine_type VARCHAR(15),
        Location VARCHAR(100),
        Owner_name VARCHAR(50),
        Average_delivery_time INT,
        contact_number VARCHAR(15),
        Total_orders INT,
        Rating FLOAT,
        IsActive VARCHAR(5)
        );
        """
        try:
            curr.execute(table)
        
            #Insert values into table using Faker
            rows=[]
            for i in range(1,self.NUM_RESTAURANTS+1):
                a=[i,self.fake_restaurant_Name(fake),
                random.choice(['Indian','South Indian','Chinese','Italian','North Indian','Mexican','American','Burmese']),
                fake.address(),fake.name(),random.choice(range(10,60)),self.fake_phone_number(fake),
                random.randint(50,1000),round(random.uniform(1,5),1),random.choice(['Yes','No'])]
                rows.append(tuple(a))
        
            insert = """
            insert into ZOMATO.RESTAURANT_TABLE
            (Restaurant_id, Restaurant_Name,Cuisine_type,Location,Owner_name,Average_delivery_time,contact_number,Total_orders,Rating,IsActive)
            values
            (%s, %s,%s, %s,%s, %s,%s, %s,%s, %s);
            """
            curr.executemany(insert, rows)
            self.db_connection.commit()

            curr.execute("select * from ZOMATO.RESTAURANT_TABLE")
            out_table=curr.fetchall()
            col = [i[0] for i in curr.description]
            self.Write_to_CSV(out_table,col,"Restaurants_Table.csv")

        except Exception as e:
            pass
        curr.close()
        return
    
    #Creating Orders Table on DB
    def Orders_table(self):
        curr = self.db_connection.cursor()
        fake = Faker(locale="en_IN")
    
        #Query to create table
        table = """
        CREATE TABLE ZOMATO.ORDERS_TABLE
        (
        Order_id INT PRIMARY KEY,
        Customer_id INT,
        Restaurant_id INT,
        Order_date VARCHAR(25),
        Delivery_time VARCHAR(25),
        Status VARCHAR(15),
        Total_amount INT,
        Payment_mode VARCHAR(15),
        Discount_Applied INT,
        Feedback_rating FLOAT,
    
        FOREIGN KEY (Customer_id) REFERENCES ZOMATO.CUSTOMER_TABLE(Customer_id),
        FOREIGN KEY (Restaurant_id) REFERENCES ZOMATO.RESTAURANT_TABLE(Restaurant_id)
        );
        """
        try:
            curr.execute(table)
           
            #Insert values into table using Faker
            rows=[]
            for i in range(1,self.NUM_ORDERS+1):
                
                #Assigning Order datetime randomly
                date_time=fake.date_time_between('-1y','now')
                order_time=date_time.strftime('%d-%m-%Y %H:%M')
        
                #Calculating Delivery datetime randomly
                new=date_time+timedelta(minutes = random.randint(10,60))
                delivery_time=new.strftime('%d-%m-%Y %H:%M')
                
                a=[i,random.randint(1,self.NUM_CUSTOMERS),
                random.randint(1,self.NUM_RESTAURANTS),
                order_time,delivery_time,random.choice(["Pending", "Delivered", "Cancelled"]),random.randint(50,5000),
                random.choice(["Credit Card","Debit Card", "Cash", "GPAY","Amazon Pay","UPI","PhonePe","Netbanking","Mobile Banking"]),
                random.randint(50,200),round(random.uniform(1,5),1)]
                rows.append(tuple(a))
        
            insert = """
            insert into ZOMATO.ORDERS_TABLE
            (Order_id, Customer_id,Restaurant_id,Order_date,Delivery_time,Status,Total_amount,Payment_mode,Discount_Applied,Feedback_rating)
            values
            (%s, %s,%s, %s,%s, %s,%s, %s,%s, %s);
            """
            curr.executemany(insert, rows)
            self.db_connection.commit()
        
            curr.execute("select * from ZOMATO.ORDERS_TABLE")
            out_table=curr.fetchall()
            col = [i[0] for i in curr.description]
            self.Write_to_CSV(out_table,col,"Orders_Table.csv")

        except Exception as e:
            pass
        curr.close()
    
        return
    
    #Creating Delivery Table on DB
    def Delivery_table(self):
        curr = self.db_connection.cursor()
    
        #Query to create table
        table = """
        CREATE TABLE ZOMATO.DELIVERY_TABLE
        (
        Delivery_id INT PRIMARY KEY,
        Order_id INT,
        Delivery_person_id INT,
        Delivery_status VARCHAR(50),
        Distance_in_kms INT,
        Delivery_time_in_min INT,
        Estimated_time_in_min INT,
        Delivery_fee INT,
        Vehicle_type VARCHAR(20),
    
        FOREIGN KEY (Order_id) REFERENCES ZOMATO.ORDERS_TABLE(Order_id)
        );
        """
        try:
            curr.execute(table)
                    
            #Insert values into table using Faker
            rows=[]
            for i in range(1,self.NUM_DELIVERIES+1):
                a=[i,random.randint(1,self.NUM_ORDERS),
                random.randint(1,self.NUM_DELIVERY_PERSONS),
                random.choice(["On the way","Delivered","Packed and Ready for take-away","Not Ready Yet","Picked up","Confirmed or ready","Rejected","Timed out"]),
                random.randint(1,15),random.randint(10,60),random.randint(10,60),
                random.randint(10,100),random.choice(["Car","Bike","Rental Bike","Rental Car","Cycle"])]
                rows.append(tuple(a))
        
            insert = """
            insert into ZOMATO.DELIVERY_TABLE
            (Delivery_id, Order_id,Delivery_person_id,Delivery_status,Distance_in_kms,Delivery_time_in_min,Estimated_time_in_min,Delivery_fee,Vehicle_type)
            values
            (%s, %s,%s, %s,%s, %s,%s, %s,%s);
            """
            curr.executemany(insert, rows)
            self.db_connection.commit()
        
            curr.execute("select * from ZOMATO.DELIVERY_TABLE")
            out_table=curr.fetchall()
            col = [i[0] for i in curr.description]
            self.Write_to_CSV(out_table,col,"Delivery_Table.csv")

        except:
            pass
        curr.close()
    
        return

    #Creating Delivery Personnel Table on DB
    def Delivery_persons_table(self):
        curr = self.db_connection.cursor()
        fake = Faker(locale="en_IN")
    
        #Query to create table
        table = """
        CREATE TABLE ZOMATO.DELIVERY_PERSONS_TABLE
        (
        Delivery_person_id INT PRIMARY KEY,
        Name VARCHAR(50),
        Contact_number VARCHAR(15),
        Vehicle_type VARCHAR(20),
        Total_deliveries INT,
        Average_rating FLOAT,
        Location VARCHAR(100)
        );
        """
        try:
            curr.execute(table)
                    
            #Insert values into table using Faker
            rows=[]
            for i in range(1,self.NUM_DELIVERY_PERSONS+1):
                a=[i,fake.name(),self.fake_phone_number(fake),
                   random.choice(["Car","Bike","Rental Bike","Rental Car","Cycle"]),
                   random.randint(50,1000),round(random.uniform(1,5),1),fake.address()]
                rows.append(tuple(a))
        
            insert = """
            insert into ZOMATO.DELIVERY_PERSONS_TABLE
            (Delivery_person_id, Name,Contact_number,Vehicle_type,Total_deliveries,Average_rating,Location)
            values
            (%s, %s,%s, %s,%s, %s,%s);
            """
            curr.executemany(insert, rows)
            self.db_connection.commit()
        
            curr.execute("select * from ZOMATO.DELIVERY_PERSONS_TABLE")
            out_table=curr.fetchall()
            col = [i[0] for i in curr.description]
            self.Write_to_CSV(out_table,col,"Delivery_Persons_Table.csv")

        except:
            pass
        curr.close()
    
        return