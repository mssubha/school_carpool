# SchoolPool 🌱 
![](file:///Users/victorsi/Desktop/Screen%20Shot%202020-03-14%20at%2012.44.09%20AM.png)
SchoolPool is a web application focused on driving children safely to school while being environmentally friendly. Parents can search a carpool buddy for their kids based on distance from their home, child’s grade, pet and smoking preferences. After finding the best carpooler, a request can be sent via the web application and a SMS will be sent to the carpooler that a request has been sent. The carpooler can view the request in the application and decide on accepting or denying it. Once a decision has been made, the carpooler who sent the request will also be notified by a SMS. Google Maps JavaScript API was used for geocoding and maps display. Twilio's programmable messaging API was used for sending text messages.<br>

## Contents
* [Features](#features)
* [Technologies & Stack](#techstack)
* [Set-up & Installation](#installation)
* [About the Developer](#aboutme)

## <a name="features"></a>  Features


## <a name="techstack"></a> Technologies and Stack
**Backend:**
Python, Flask, SQLAlchemy, PostgreSQL <br>
**Frontend:**
Javascript, jQuery, Bootstrap, Google Fonts, HTML, CSS <br>
**APIs:**
Google Maps Javascript API, Google Geocoding API, Twilio API



## <a name="installation"></a> Set-up & Installation
Install a code editor such as [VS code](https://code.visualstudio.com/download) or [Sublime Text](https://www.sublimetext.com/).<br>
Install [Python3](https://www.python.org/downloads/mac-osx/)<br>
Install [pip](https://pip.pypa.io/en/stable/installing/), the package installer for Python <br>
Install [postgreSQL](https://www.postgresql.org/) for the relational database.<br>


Clone or fork repository:
```
$ git clone https://github.com/mssubha/school_carpool
```
Create and activate a virtual environment inside the schoolpool directory:
```
$ virtualenv env
$ source env/bin/activate
```
Install dependencies:
```
$ pip3 install -r requirements.txt
```
Make an account with [Google](https://developers.google.com/maps/documentation/javascript/overview) & get an [API key](https://developers.google.com/maps/documentation/javascript/get-api-key).<br>
Make an account with [Twilio](https://www.twilio.com/docs) & get an [API key](https://www.twilio.com/docs/usage/api).<br>

Store these keys and the Twilio string Identifier (SID) in a file named 'secrets.sh' <br> 
```
$ source secrets.sh
```
With PostgreSQL, create the SchoolPool database
```
$ createdb dbschoolpool
```
Enter the database
```
$ psql dbschoolpool
```
While inside the database, run postgis extension before creating tables.
```
dbschoolpool=# CREATE EXTENSION postgis;
```
Create all tables and relations in the database and seed all data:
```
$ python3 model.py
$ python3 seed_database.py
```
Run the app from the command line:
```
$ python3 server.py
```


## <a name="aboutme"></a> About the Developer

