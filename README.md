## Kul-Balam (Fast API + Python)
### Project Description
This is the backend for Kul-Balam, a social network project with a marketplace. The backend is built using FastAPI for high-performance, asynchronous operations. It handles user interactions, marketplace functionalities, and image management.

### Getting Started
Follow these instructions to get the project up and running on your local machine for development and testing purposes.

### Prerequisites
Make sure you have the following installed:

Python (>= 3.7)

pip (Python package installer)

### Installation
Clone the repository
Navigate to the project directory
Install the dependencies: npm install

### Running the Project
1. Install the requirements
-----------------------------------
pip install -r requirements.txt
-----------------------------------

2. Create the folders for the images
----------------------------------
mkdir images
mkdir productimages
-----------------------------------

3. Run the program
-----------------------------------
uvicorn main:app --reload
-----------------------------------

4. Open Swagger

http://localhost:8000/docs

### API Documentation
FastAPI automatically generates interactive API documentation using Swagger. To view it:

Open your browser and navigate to:

http://localhost:8000/docs

### Built With
FastAPI - Modern, fast (high-performance) web framework for building APIs with Python.

Uvicorn - Lightning-fast ASGI server for serving FastAPI applications.

Python - Backend programming language.
