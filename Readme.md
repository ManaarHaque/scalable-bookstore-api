#  **Project Assignment: MongoDB & Flask on Kubernetes**

## **Course: AIN-3003 Database Systems and Cloud Computing**

**Submitted by: Manaar Haque 2357276**

Due Date: January 12, 2026

# Overview

This is my submission for the "Option 1" project assignment. I built a containerized Python Flask application that acts as a Bookstore API. It connects to a MongoDB database, and the whole system is orchestrated using Kubernetes.

### The project demonstrates:

* Containerization of a Python app using Docker.

* StatefulSets for persistent database storage (MongoDB).

* Deployments for the stateless application logic.

* Service Discovery so the app can talk to the database automatically.

### Project Structure

Here is a quick breakdown of the files in this project:

* **app.py**: The main Python application code using Flask and PyMongo. It handles all the CRUD operations (Create, Read, Update, Delete).

* **Dockerfile**: The instructions for Docker to build the image for our Python app.

* **requirements.txt**: List of Python dependencies (flask, pymongo).

* **Mongodb.yaml**: Kubernetes configuration for the database. It includes a StatefulSet (to keep data safe) and a Service (to expose it internally).

* **deployment.yaml**: Kubernetes configuration for the web app. It creates a Deployment and a LoadBalancer Service to expose the app to the outside world.

* **bookstore.json**: Data used for the application.

# Installation & Setup Guide

## Prerequisites:

* Docker
* Kubernetes Cluster (Minikube, Docker Desktop, or a cloud provider)
* kubectl CLI tool configured to talk to your cluster

## Step 1: Build and Push the Docker Image

First, we need to package the Python application into a Docker container.

Open your terminal in the project folder.

1. **Add your own username:**

```bash 
docker build -t your-dockerhub-username/bookstore-app:latest .
```


2. **Push the image to Docker Hub so Kubernetes can pull it:**
```bash
docker push your-dockerhub-username/bookstore-app:latest
```

Important: Before moving to the next step, open deployment.yaml and find the line image: manaarishere/bookstore-app:latest. Change it to your own image name (e.g., your-dockerhub-username/bookstore-app:latest) if you want to use the one you just built.

## Step 2: Deploy MongoDB

We need the database running before the app can connect to it.

1. **Apply the MongoDB configuration:**
```bash
kubectl apply -f Mongodb.yaml
```

2. **This creates a Service named mongodb-service and a StatefulSet named mongodb. You can check if it's ready:**
```bash 
kubectl get pods
```
*Wait until you see mongodb-0 with status "Running"*

## Step 3: Deploy the Flask Application
Now we deploy the API itself.

1. **Apply the application configuration:**
```bash
kubectl apply -f deployment.yaml
```

*This creates a Deployment named flask-app and a Service named flask-service.*

2. **Check the status of everything:**
```bash
kubectl get all
```

## How to Use the API

Once everything is running, you need to access the flask-service.
*Using Docker Desktop/Localhost: It should be available at http://localhost:80.*

### Below are example commands to test the endpoints. 

1. Check Status

Simple check to see if the app acts to the DB.

```bash
curl http://localhost:80/
```


Response: {"status": "App is running", "db_status": "Connected"}

2. Add a Book (Create)

Let's add a new book to the store.

```bash
curl -X POST -H "Content-Type: application/json" -d '{
    "isbn": "978-0132350884",
    "title": "We Hunt The Flame",
    "author": "Hafsah Faizal",
    "year": 2019
}' http://localhost:80/books
```


3. Get All Books (Read)

Retrieve the list of books.

```bash
curl http://localhost:80/books
```


4. Update a Book (Update)

**Change the title of the book we just added.**

```bash
curl -X PUT -H "Content-Type: application/json" -d '{
    "title": "We Free The Stars"
}' http://localhost:80/books/978-0132350884
```


5. Delete a Book (Delete)

**Remove the book from the database.**

```bash
curl -X DELETE http://localhost:80/books/978-0132350884
```


Bonus: Initialize Data

**I also included a script to seed the database with the bookstore.json data.**

```bash
curl -X POST -H "Content-Type: application/json" -d @bookstore.json http://localhost:80/init
```


## How it works

1. **Service Discovery:** The Python app knows where the database is because I defined environment variables in deployment.yaml. Specifically, MONGO_HOST is set to mongodb-service. Kubernetes DNS resolves this name to the internal IP of the MongoDB pod.

2. **Persistence:** The MongoDB StatefulSet uses a VolumeClaimTemplate. This ensures that even if the MongoDB pod crashes or restarts, the book data is saved to a Persistent Volume and isn't lost.

3. **Load Balancing:** The flask-service is type LoadBalancer, which distributes incoming traffic to the available application pods.

