# DataProject
Simple Ticketing App build using SQLITE, FLASK and Docker

Prerequisites:
Docker and Docker Compose needs to be installed 

Folder Structure:
```
Data Project
|
|-- TicketingDataModel.PDF
|
|--vivid
|    |
|    |-api
|    |   |
|    |   |-app.py
|    |   |-requirements.txt
|    |
|    |-data
|    |   |-event.db [this will be created when the code is run]
|    |
|    |-db
|    | |
|    | |-setup.py
|    |
|    |-load
|        |
|        |-load.py
|        |-sampleTickets.csv
|
|--Dockerfile
|
|--docker-compose.yml    
```
 Description About Project:
 
 Used SQLITE for database because loading for it is very fast and the creating docker image using it is faster. Since the data set used for the demo project was small hence sqlite was used, however it can be easily replaced with mysql or postgresql. 
 
 Clone the project and change to the vivid directory and then run the following command to start the project:
 
 ```docker-compose up```
 
 The above command starts the docker and create three containers:
 
 - First container which creates the event.db in the data folder. It calls setup.py
 - Second conatiner is the web container and runs the flask application and calls app.py
 - Third container loads data into events.db. It calls the scripts load.py
 
 The flask application runs on 0.0.0.0:5000 or locahost:5000. It has following methods:
 
 - GET all events. URL for it http://0.0.0.0:5000/events 
 - GET all tickets for an event. The URL for it is http://0.0.0.0:5000/events/<event-id>/tickets, example url http://0.0.0.0:5000/events/164/tickets
 - GET best tickets for an event. The url for it is http://0.0.0.0:5000/events/<event-id>/tickets/best. Example URL for it http://0.0.0.0:5000/events/164/tickets/best . Best ticket is calculated based on the most expensive ticket for an event.
 - To post a ticket for seller, use curl command or a tool like POSTMAN, example command is curl -H "Content-type: application/json" -X POST http://127.0.0.1:5000/seller  -d '{"eventid":"107","id":"2","card":"11111","price":"200","sectionid":"90","rownumber":"RR","seatnumber":"2"}'
 - To update the ticket sell out use the curl or POSTMAN. Example command  curl -H "Content-type: application/json" -X PUT  http://127.0.0.1:5000/events/107/soldout  -d '{"sectionid":"203","rownumber":"8"}'
 
Docker compose is used to manage the three container images and they share the common volumes

Debugging:

If in case any issue happens use the below commands to stop the docker containers.

```docker-compose down```

```docker system prune -f```

```docker rmi $(docker images -q) -f```

Also truncate all the tables in event.db if you need to restart the docker-compose or just simply delete it from the folder data. As on restart the load.py would be executed and otherwise would fail with 'unique identity constraint'

if incase you get error related to database been lock. It can be identified by using below command:

```fuser event.db```

```kill -9 spid```
