######This setups the database and creates the tables
import sqlite3 as sqlite
from sqlite3 import Error
import sys
import os
import csv

#Methd to create database
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

#Method to create tables
def create_table(conn, create_table_sql):

    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

#Main method with table definitions
def main():
    database = r"../data/events.db"

    sql_create_events_table = """ CREATE TABLE IF NOT EXISTS event (
                                            eventid integer PRIMARY KEY,
                                            venueid integer,
                                            eventname text ,
                                            event_startdate text,
                                            event_enddate text
                                        );
                                        """
    sql_create_venue_table = """ CREATE TABLE IF NOT EXISTS venue (
                                                venueid integer PRIMARY KEY,
                                                venuename text,
                                                venuecapacity integer,
                                                addressid integer
                                            );
                                            """
    sql_create_section_table = """ CREATE TABLE IF NOT EXISTS section (
                                                sectionid integer,
                                                venueid integer,
                                                totalseats integer ,
                                                rownumber text,
                                                seatsavailable integer,
                                                priceperseat float,
                                                soldoutflag text
                                            );
                                            """

    sql_create_customer_table = """ CREATE TABLE IF NOT EXISTS customer (
                                                   customerid integer PRIMARY KEY,
                                                   addressid integer,
                                                   name text ,
                                                   gender text,
                                                   emailid text,
                                                   password text,
                                                   creditcarddetails integer,
                                                   refferaldetails text
                                               );
                                               """
    sql_create_address_table = """ CREATE TABLE IF NOT EXISTS address (
                                                     addressid integer PRIMARY KEY,
                                                     addressline1 text ,
                                                     city text,
                                                     state text,
                                                     country text,
                                                     phone text
                                                 );
                                                 """

    sql_create_reservation_table = """ CREATE TABLE IF NOT EXISTS reservation (
                                                         reservationid integer PRIMARY KEY,
                                                         orderid integer ,
                                                         sectionid integer,
                                                         venueid integer,
                                                         SeatsBooked integer,
                                                         TotalPrice integer
                                                     );
                                                     """

    sql_create_orders_table = """ CREATE TABLE IF NOT EXISTS orders (
                                                             ordersid integer PRIMARY KEY,
                                                             customerid integer ,
                                                             eventid integer,
                                                             orderstatus text,
                                                             orderdate text
                                                         );
                                                         """
    sql_create_seller_table = """ CREATE TABLE IF NOT EXISTS seller (
                                                                 sellerid integer,
                                                                 eventid integer ,
                                                                 creditcarddetails integer,
                                                                 sellingprice text,
                                                                 sectionid integer,
                                                                 seatnumber integer
                                                             );
                                                             """

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_events_table)
        create_table(conn, sql_create_venue_table)
        create_table(conn, sql_create_section_table)
        create_table(conn, sql_create_customer_table)
        create_table(conn, sql_create_address_table)
        create_table(conn, sql_create_reservation_table)
        create_table(conn, sql_create_orders_table)
        create_table(conn, sql_create_seller_table)

    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()

