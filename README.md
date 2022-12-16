# Collect Central

This repository contains the code for the Collect project designed for atlan

Completed Work:
- Creation of form
- Submission of response
- Entering response into a google sheet upon submission of response
- Sending a message to the user using Twilio API upon
submission of response

Pending work:
- Complete TODO's
- The dockerfile has some errors that need to be fixed
- Add support for validation
- Modify some of the methods to catch errors in a better way
- Modify the parameters of sem methods and method calls
- Fix loadtesting errors

# The API design specification can be found in the file
```
api_spec.json
```
in the root directory of the project

# Approaches

- ## Fast API or Django rest framework with PostgreSQL backend:

    - Initially, I thought of using a Relational database as a backend and tried to come up with a schema but when going through the use cases I found that designing a schema that fits all the use cases and allows for future modifications would be hard and adding new services would either require a complete overhaul of the schema or a lot of migration scripts

    - I refrained from using Django rest framework to design the API as Fast API allowed me to test the API easily and the setup was easier

# Chosen Approach

## Fast API with MongoDB backend:

The Forms submitted by the form creator are added to MongoDB and upon receiving a response the appropriate tasks are performed by adding them to a task_queue

The forms submitted by the user are stored in a MongoDB collection with the following schema

```json
{
    "title": "<form_title>",
    "questions": {
        "KEY1": "question1",
        "KEY2": "question2",
        ...
        ...
    },
    "validate": {
        "KEY1": "validation",
        "KEY2": "validation"
    },
    "tasks": [
        "SMS",
        "SHEETS",
        ...
    ],
    "form_owner": "<form_owner_email>"
}
```

The data is received from the creator of the form in the request body and inserted into the database

## **Keys:**

### **questions:**

The questions key in the JSON contains key value pairs of the format
```json
"KEY": "question"
```
The **KEY** is used to insert the response to the question in the response collection and also make it easily searchable

This **KEY** can be provided by the user or determined by the frontend by using the title

### **validate:**

The validate key in the JSON contains key value pairs of the format
```json
"KEY": "validate"
```
where **KEY** is the key associated with the question and validate is a custom syntax for validating the data based ont he user requirement

### **tasks:**

Contains an array of strings indicating the tasks that need to be perfomed upon submission of a response from the user

The responses are stored in a MongoDB collection in the format

```json
{
    "form_title": "<form_title>",
    "form_id": "<form_id>",
    "KEY1": "value",
    "KEY2": "value"
}
```

Since task_queue is being used with Redis as the message broker the API ensures high availability

I have also added sentry for monitoring the API and I have also setup some basic logging.


### **Pros:**
-  This allows for maximum customization and easier updating as the backend is not schema bound
- Services can be added to the /backend/services directory and can be called by modifying the logic of /backend/tasks/task_scheduler to call the service with the appropriate parameters which allows for a plugin fashion
- Allows for maximum customization of request handling which can be beneficial to serve the use cases of all users

### **Cons:**
- Maintaining the MongoDB specification and documenting the JSON schema for the request and response bodies is hard
- Upgrading from an existing API configuration with backward compatibility might be hard
- Extensive documentation needs to be provided
- Creating and managing a custom validation syntax for validating the data can be hard

# How to run:

- If not installed, Install Docker desktop on your computer
- Create a mongodb instance using the command
    ```
    docker run --name mongodb -d -p 27017:27017 mongo
    ```
- Create a redis instance using the command
    ```
    docker run --name some-redis -d -p 6379:6379 redis
    ```
- With pipenv:
    - run the following command to install all libraries
        ```
        pipenv install
        ```
    - activate the virtual environment using
        ```
        pipenv shell
        ```
- With pip:

    - Create a virtual environment and install the requirements in requirements.txt using:
        ```
        pip install -r requirements.txt
        ```
- Add Twilio API keys to .env file in the root folder
    ```
    TWILIO_ACCOUNT_SID=<account_sid>
    TWILIO_AUTH_TOKEN=<auth_token>
    ```
- Add google cloud service account credentials in service_cred.json file in the root folder
- Activate virtual environment and run redis worker using the command:
    ```
    rq worker --with-scheduler
    ```
- In another shell, Activate virtual environment and start the API using:
    ```
    python main.py
    ```
