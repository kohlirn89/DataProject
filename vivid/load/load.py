# It used the csv and loads the data into the database
import sqlite3
import csv
import time

with open('sampleTickets.csv', 'r') as f: # This Opens CSV in read mode
    reader = csv.reader(f) #reading line by line
    report_list = list(reader) #converts it into a list
final_list = report_list[1:] #removing header

eventids=[]

for row in final_list:
    if row[0] not in eventids:
        eventids.append(row[0]) #finding distinct values for events

time.sleep(2)
# added this sleep time as sometimes the script was executing before the tables were created.
# if you experience the same then increase this time
for ids in eventids:
    #Setting up dummy values each event wise. This can be made dynamic by creating a csv and loading it from there
    if ids == '162':
        eventname = 'Cubsgame'
        venueID = 1
        AddressID = 100
        venueName = 'Wrigley Field'
        eventStartDate = '01-01-2019'
        eventEndDate = '01-31-2019'
        venueAddress = '1060 W Addison St'
        City = 'Chicago'
        State = 'Illinois'
        venueCapacity = 15000
    elif ids == '164':
        eventname = 'Hamilton'
        venueID = 2
        AddressID = 200
        venueName = 'CIBC Theatre'
        eventStartDate = '03-01-2019'
        eventEndDate = '10-31-2019'
        venueAddress = '18 W Monroe St'
        City = 'Chicago'
        State = 'Illinois'
        venueCapacity = 500
    else:
        eventname = 'BlackHawksGame'
        venueID = 3
        AddressID = 300
        venueName = 'United Center'
        eventStartDate = '01-10-2019'
        eventEndDate = '06-20-2019'
        venueAddress = '1901 W Madison St, Chicago, IL'
        City = 'Chicago'
        State = 'Illinois'
        venueCapacity = 10000

    conn = sqlite3.connect('../data/events.db', timeout=10)
    cur = conn.cursor()

    #Loading Event Table
    eventLoad = ('''INSERT INTO event (eventid,venueid,eventname,event_startdate,event_enddate) 
            VALUES (%s,%s,%s,%s,%s);''' % (ids, venueID, "'" + eventname + "'", "'" + eventStartDate + "'", "'" + eventEndDate + "'"))
    cur.execute(eventLoad)

    #Loading Venue Table
    venueLoad = ('''INSERT INTO venue (venueid,venuename,venuecapacity,addressid) 
            VALUES (%s,%s,%s,%s);''' % (venueID, "'" + venueName + "'", venueCapacity, AddressID))
    cur.execute(venueLoad)

    #Loading Address Table
    addressLoad = ('''INSERT INTO address (addressid,addressline1,city,state,country)
            VALUES (%s,%s,%s,%s,'USA');''' % (AddressID, "'" + venueAddress + "'", "'" + City + "'", "'" + State + "'"))
    cur.execute(addressLoad)

    #Load for Section tables
    for record in final_list:
        if ids in record[0]:
            SectionId = record[1]
            quantity = record[2]
            price = record[3]
            rowNumber = record[4]
            sectionLoad = ('''INSERT INTO section (sectionid,venueid,totalseats,rownumber,seatsavailable,priceperseat,soldoutflag) 
            VALUES (%s,%s,20,%s,%s,%s,'Available');''' % (SectionId, venueID, "'" + rowNumber + "'", quantity, price))
        # print(sql3)
            cur.execute(sectionLoad)
            conn.commit()
    cur.close()
    conn.close()


