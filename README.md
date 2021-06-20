# BoardMeServer
Backend for the board me bus application. A small application built with a concept to solve issues with public transport for hackathon conducted by Nasdaq and hackerearth. Application built around beacon technology to help address public transportation booking issue with smart phones and better use of tech in minimising troubles.
Please go through the problem statement [here](./ProblemStatement.md)



### The architecture:
![Architecture](./images/BoardMeArchitecture.png)

### The schema:
![Schema](./images/boardme_schema.png)


### The BigPicture:
![BeaconTech](https://github.com/rajagopal28/TheGimbalStore/raw/master/images/image10.png)


### The Flows:
#### BoardMe:
This is the flow in which the user boards a bus and pays through the app.
1. The user board the bus which has a beacon planted to it.
2. User opens the app and clicks board.
3. The system picks the nearest beacon as the reference.
4. The system pick the user location and send the data to the server.
5. The server computes the nearest stop in the route that the beacon belongs to and prompts the following destinations for him/her to choose.
6. The user choose the destination and pays through his app wallet.
7. The user travel history is recorded with the location that the user has boarded.
8. The user also receives a SMS confirmation.
#### BoardWait:
This is the flow in which the user boards a bus and pays through the app.
1. The user opens the app and choses the route he/she wishes to travel.
2. App send the user location and the chosen route to the server.
3. Server finds the stop, closest to the user, in the chosen route and computes the ETA though google API.
4. The app renders the ETA response from the server.

## Steps to run the application
### installing the packages
- `` cd board-me-server ``
- run the command `` pip install --upgrade -r requirements.txt ``
- use `` sudo `` if fails with permission issues

### running server
- `` python run-local.py ``

### running integration tests
- `` python run-tests.py ``

## Technical nuances
 - **Flask:** Have worked with python flask before. It is one of the light weight easy to setup library to create rest api applications in a whip of time. It is reliable, quick to deploy and easy to setup.
 - **SQLite:** Needed a totally light weight easy to load and save backend. SQLite was or first choice. It is a file based system. As our requirement just involved only little amount of data we chose this.
 - **SQL Alchemy:** SQL Alchemy is one of the easy to use backend libraries that goes well with Flask. It helped big time in creating modeling data and associating relationship with less backend code and more ORM python codes.
 - **Integration tests:** For the first time in forever, I have written integration test for the service endpoints and integrated as part of the release phase in the heroku dyno. This was made possibile with temporary files and the file based SQLite backend support.



## User Views:
### Home
![Home](./images/web-home.png)

### Login
![Login](./images/web-login.png)

### Users
![UsersList](./images/web-users.png)

### UserInfo
![UserInfo](./images/web-user-info.png)

### Routes
![Routes](./images/web-routes.png)

### BoardWait
#### Choose Bus/Route
![ChooseRoute](./images/web-board-wait-1.png)

#### Choose Boarding
![Boarding](./images/web-board-wait-2.png)

#### Choose Destination
![Destination](./images/web-board-wait-3.png)

#### Ticket Confirmation
![TicketConfirmation](./images/web-ticket-confirmation.png)


### BoardingHistory
![History](./images/web-travel-history.png)


### References:
The following are the references that has been used in the above detailed documentation:
#### Tech:
* Python-Flask-Mysql: http://code.tutsplus.com/tutorials/creating-a-web-app-from-scratch-using-python-flask-and-mysql--cms-22972
* Openshift deployment of Python:  https://github.com/caruccio/openshift-flask-mysql-example
* Material Design in android: http://developer.android.com/design/material/index.html
* Retrofit library of network calls in android:https://github.com/codepath/android_guides/wiki/Consuming-APIs-with-Retrofit
* Estimote beacons:  http://developer.estimote.com/eddystone/ https://github.com/estimote/android-sdk#quick-start-for-eddystone
* Architecture diagram: https://www.draw.io/
* Schema creation: http://www.vertabelo.com
* Twilio: https://www.twilio.com/docs/api  
* GoogleAPIClient for android: https://developers.google.com/android/guides/api-client
#### Statistical:
* Statistical reference on transportation in Chennai: http://www.cmdachennai.gov.in/pdfs/CCTS_Executive_Summary.pdf
* Article in The hindu: http://www.thehindu.com/news/cities/chennai/public-transport-system-chennai-has-miles-to-go/article1143993.ece
* Traffic stat in Chennai: http://chennaicityconnect.com/chennai-pedia/statistics/traffic-transportation/
