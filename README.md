CIS 322 Project 6
Jacob Rammer
jrammer@uoregon.edu


This project creates a controle time calculator, database storage, and restfull api integration.

How to use (if using supplied docker file):

localost:5000 will bring up the ACP calculator

NOTE: For some reason the JSON data is being sorted by the browser or 
something else alphabetically. When debugging in Python, the JSON datatypes 
are represented correctly. I gave up after a few hours of debugging. 

API: shows data in JSON or CSV form
CSV Note: The csv format is rendered as a string, remove quotes appropriately!

How to use: localhost:5000/listAll will list all entries in the database in JSON format.

localhost:5000/listAll/json is treated the same as /listAll since the data is in
JSON format initially. This behavior is also the same for /listOpenOnly/json, /listClosedOnly/json.

localhost:5000/listOpenOnly will return the brevets with only the open times

localhost:5000/listClosedOnly will return the brevets with only the closed times

localhost:5000/listAll/csv will display the brevets in CSV format where each new entry is denoted by "new_entry" with "k" km, open, close values. K being number of controle points in the brevet

localhost:5000/listOpenOnly/csv will return controle times with open data only in csv format

localhost:5000/listClosedOnly/csv will return controle times with closed data only in csv format

localhost:5000/listOpenOnly/csv?top=3 will return the top 3 results in csv form

localhost:5000/listOpenOnly/json?top=5 will return 5 results in json format

localhost:5000/listClosedOnly/json?top=4 will return 4 results in json format

Website: localhost:5000
localhost:5000/listAll will bring up a list of all info in the database. Lists all,
only open, and only closed controle times.

In order to run this on your local machine, you will need to
create .env files within both the api and brevet_calculator
folders with a single key SECRET_KEY=your_secret_key

