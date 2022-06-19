# Wadi-7alfa
This is an Integration between clickup and a local database, using clickup webhooks 

## How does it work
You need to add Token , task_id and server url to webhook/create and then comment all the function except create_web dunction and then run the script and it will create the webhook
and then you need to add token and task_id(will be found in the url of clickup when you are getting the token
Our server will save any task created in clickup and will save the following entries
*Task ID
*Name
*Description
*status
*hours worked on the project

and when a subtask is created it will save
*ID
*Name
*Description
*Parent

It does that because we provided an Endpoint to recive the data by the name of Clickup in back/views.py
and a function to parse the data and know the type of the data (task created, task updated, sub task created and subtask updated) the name of the function is request_router in back/views.oy
once we know the nature of the data sent by clickup we send the data to a specialized function that save the data in our DB

to take a look at the data go to tasks/ and subtasks/
