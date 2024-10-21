![image](https://github.com/user-attachments/assets/8bbf4ec5-086c-4b8a-baf9-b85c2c9474f6)﻿# Project Setup

##1. Clone the Repository
First, clone the repository:

git clone git clone <https://github.com/petrukv/User-Actions-With-AI-API.git>  
cd <project_folder_name>  

## 2. Create and Activate a Virtual Environment  
# Create a virtual environment
python -m venv .venv

# Activate the virtual environment:
.\.venv\Scripts\activate

## 3. Install Dependencies  
pip install -r requirements.txt

## 4. Configure the Database  
 # Create a .env file containing all the fields from .env.sample

## Running the Project
uvicorn app.main:app --reload

## API Review  
#Create User
![image](https://github.com/user-attachments/assets/4aae90ea-68cc-40c3-8452-c612fdc2a04a)
in auto_reply_delay we put minutes and it stands for auto reply to the comments under post. If 0, this function if deactivated, if > 0, activated 


#Login 
![image](https://github.com/user-attachments/assets/251da6fd-ae91-42b4-a1b4-222219f94763)

##After that you should copy access_token and paste it in app/tests/test_user.py in headers after Bearer
![image](https://github.com/user-attachments/assets/c779e793-73c7-4c30-bbbb-9a5e7573eaf3)

# Create post (make sure that you use token in headers)
![image](https://github.com/user-attachments/assets/6fd35e81-8c1e-422d-ad3d-5dc30efe9018)

## Create post with this example {
        "title": "Test Post",
        "content": "This is a test post"
    }

# Create comment (make sure that you use token in headers)
![image](https://github.com/user-attachments/assets/f98da51f-b2a1-4c7c-9b65-139bc4991707)
feel free to create 4 comments for testing

# Analytics (http://127.0.0.1:8000/user/comments-daily-breakdown?date_from=2024-10-01&date_to=2024-10-31)
![image](https://github.com/user-attachments/assets/f658553a-0a02-477c-8dbf-449e1e7d697a)

## pytest will launch all tests  
make sure that you create 1 post 
