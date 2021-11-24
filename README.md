CIS 322 Project 6
Jacob Rammer
jrammer@uoregon.edu


This project creates a controle time calculator, database storage, and restfull api integration.

How to use (if using supplied docker file):

localost:5000 will bring up the ACP calculator

NOTE: For some reason the JSON data is being sorted by the browser or 
something else alphabetically. When debugging in Python, the JSON datatypes 
are represented correctly. I gave up after a few hours of debugging. 

API: shows data in JSON or CSV form localhost:5002
CSV Note: The csv format is rendered as a string, remove quotes appropriately!

How to use: localhost:5002/listAll will list all entries in the database in JSON format.

localhost:5002/listAll/json is treated the same as /listAll since the data is in
JSON format initially. This behavior is also the same for /listOpenOnly/json, /listClosedOnly/json.

localhost:5002/listOpenOnly will return the brevets with only the open times

localhost:5002/listClosedOnly will return the brevets with only the closed times

localhost:5002/listAll/csv will display the brevets in CSV format where each new entry is denoted by "new_entry" with "k" km, open, close values. K being number of controle points in the brevet

localhost:5002/listOpenOnly/csv will return controle times with open data only in csv format

localhost:5002/listCloseOnly/csv willl return controle times with closed data only in csv format

localhost:5002/listOpenOnly/csv?top=3 will return the top 3 results in csv form

localhost:5002/listOpenOnly/json?top=5 will return 5 results in json format

localhost:5002/listCloseOnly/json?top=4 will return 4 results in json format

Website: localhost:5001
localhost:5001 will bring up a list of all info in the database. Lists all, 
only open, and only closed controle times.

localhost:5001/listOpen.php will list controle open times only

localhost:5001/listClosed.php

