# **COMP2001 — Assessment 2**

This is a repository for my **COMP2001 Assessment**. It contains all the files for the microservice I implemented for the trail service. My microservice implements CRUD functionality for trails and authentication for users using JWT tokens.

---

## **Repository Structure**

- **`/api/Trail.py`**  
  Contains the CRUD functions for trail management.

- **`/App.py`**  
  Contains database configuration and initializes the Flask and Connexion apps.

- **`/Authentication.py`**  
  Implements JWT authentication and integrates with the external authenticator service.

- **`/Dockerfile`**  
  Defines the Docker deployment setup for containerizing the application.

- **`/Models.py`**  
  Defines all the database tables and their relationships.

- **`/requirements.txt`**  
  Lists all the required libraries and dependencies for the project.

- **`/Swagger.yml`**  
  Contains OpenAPI documentation for the login, authentication, and CRUD operations endpoints.

---

## **Swagger Endpoints**

### **Authentication**
- **`POST /login`**  
  User authentication, returns a JWT token.

### **Trails Management**
- **`GET /Trails`**  
  Retrieve all trails.

- **`POST /Trails`**  
  Create a new trail.

- **`GET /Trails/{Trail_ID}`**  
  Retrieve a trail by ID.

- **`PUT /Trails/{Trail_ID}`**  
  Update a trail by ID.

- **`DELETE /Trails/{Trail_ID}`**  
  Delete a trail by ID.

---
