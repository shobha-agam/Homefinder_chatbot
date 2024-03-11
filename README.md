# Homefinder_chatbot

HomeFinder Chatbot Project – project setup

1.	Backend: FASTAPI
1.	Create virtual environment:
o	Python -m venv chatbotenv
o	Activate: chatbotenv\Scripts\activate

2.	To run the project give command in terminal
Python main.py
o	To access all API use this url:
o	http://localhost:8000/chatbot/docs

3.	Install all the dependencies:
o	Pip install fastapi
o	Pip install uvicorn
o	Pip install sqlalechemy
o	Pip install requests
o	Pip install passlib
o	pip install python-multipart
o	pip install python-jose
o	Pip freeze>requirements.txt

4.	Install all the dependencies for PostgreSQL
o	Pip install psycopg2
o	Pip install alembic
o	Initialize alembic: alembic init alembic
o	alembic revision –autogenerate
o	alembic upgrade head

5.	Install dependencies for NLP:
o	Pip install nltk

6.	Install dependencies for Testing:
o	Pip install pytest
o	To run test cases give  command in terminal:
	Pytest test_main.py -v -s
	To check code coverage : Pytest --cov
	Coverage report -m

2.	Frontend: React-JS
1.	To run the project give command in terminal 
o	npm install.
2.	Install all the dependencies:
o	npm install react-router-dom
o	npm install axios
o	npm install react-hook-form
o	npm install @mui/material @emotion/react @emotion/styled
o	npm install @mui/material @mui/styled-engine-sc styled-components
To run project – npm start







 
