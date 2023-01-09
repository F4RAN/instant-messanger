# instant-messanger
## Installation:
‍‍‍‍in the root folder:

`pip3 install requirement.txt`

and after installation:

`flask run`

in the /root/ui folder:

`npm i`

after installation:

`npm run dev`

## Run project:
you need install kafka in your os, then you should use these commands for create and moderate kafka topic:

`kafka-topics --bootstrap-server 127.0.0.1:9092 --topic INSTANT --create --partitions 3 --replication-factor 1`

you should see "INSTANT" topic in topics list:

`kafka-topics --list --bootstrap-server 127.0.0.1:9092`

you must run kafka_consumer.py file separately (in root):

`python3 kafka_consumer.py`
## Basic FEATURES:

:white_check_mark:	implement a socket io messanger

:white_check_mark:	messanger can emit messages to server

:white_check_mark:	server can process and filter some words like profanity, etc.

:white_check_mark:	server emit back message to other end user (include filtered words),

:white_check_mark: stream proccessing cencor function 	

:white_check_mark: spam detection function (send more than 5 messages in 5* second detected as a spam < * For test reasons you can change it in check_spam() function)

## Additional FEATURES:

:white_check_mark:	1- Messages stores in the database,

:white_check_mark:	2- Messages creation time, 

:white_check_mark:	3- Representation of friends list,

:white_check_mark:	4- latest message of each friend representation, 

:white_check_mark:	5- Register and Authentication with mobile number and set cookie for future login (JWT),

:white_check_mark:	6- Show unread messages on a counter in the corner of a friend's card,

:white_check_mark:	7- Add friends to the friends list with phone number, 

:white_check_mark:	9- representation of sent messages by check sign and seen messages by double check sign,

:white_check_mark:	10- when you chatting with a friend messanger can keep the message from other friends,

:white_check_mark:	11- Reperesentation of user messages history

## Main programming languages, frameworks/libs and db:
1- Python

2- Javascript

3- Vue/Nuxt

4- Flask

6- SocketIO

7- MongoDB