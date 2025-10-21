# 🧠 Django String Analyzer API

A RESTful API service built with **Django REST Framework**, designed to analyze strings and compute their properties.  
This project is part of the **Backend Wizards – Stage 1 Task**.

---

## 🚀 Features

For every analyzed string, the API computes and stores:

- ✅ **Length** — number of characters  
- ✅ **Palindrome check** — whether the string reads the same backward  
- ✅ **Word count** — number of words in the string  
- ✅ **Unique characters** — total number of distinct characters  
- ✅ **Character frequency map** — frequency of each character  
- ✅ **SHA256 hash** — unique hash for deduplication  

Additionally:
- Supports **natural language filtering** (e.g., _“all single word palindromic strings”_)
- Provides **list, detail, and delete** endpoints  
- Uses **SQLite locally**, **PostgreSQL on Railway**
- Supports **Whitenoise static serving** for production  

---

## 🧩 Tech Stack

- **Python 3.12+**
- **Django 5.2**
- **Django REST Framework**
- **Whitenoise**
- **dj-database-url**
- **Railway Deployment**

---

## 🏗️ Setup & Installation
###1️⃣ Clone the Repository
git clone https://github.com/Betty20000/string-analyzer.git
cd string-analyzer

### 2️⃣ Create Virtual Environment
python -m venv venv


Activate it:

Windows

venv\Scripts\activate


Mac/Linux

source venv/bin/activate

### 3️⃣ Install Dependencies
pip install -r requirements.txt

## ⚙️ Configure Environment Variables

Create a .env file in the project root:

SECRET_KEY=django-insecure-yourkeyhere
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost


When deployed on Railway, these variables will be automatically injected:

`DATABASE_URL`
`DEBUG=False`
`ALLOWED_HOSTS=*`
`DISABLE_COLLECTSTATIC=0`

## 🧠 Running the Project Locally
Run Migrations
python manage.py makemigrations
python manage.py migrate

Start the Server
python manage.py runserver


Then open:
👉 http://127.0.0.1:8000/

## 🔗 API Endpoints
### 1️⃣ POST /strings/ — Analyze a new string

Request

{
  "value": "racecar"
}


Response (201 Created)

{
  "id": "<sha256>",
  "value": "racecar",
  "properties": {
    "length": 7,
    "is_palindrome": true,
    "unique_characters": 4,
    "word_count": 1,
    "sha256_hash": "<sha256>",
    "character_frequency_map": {"r":2,"a":2,"c":2,"e":1}
  },
  "created_at": "2025-10-21T12:34:56Z"
}

### 2️⃣ GET /strings/ — List all analyzed strings

Supports filters:

Parameter	Description
is_palindrome	true / false
min_length	Minimum string length
max_length	Maximum string length
word_count	Exact word count
contains_character	Character substring

Example:

GET /strings/?is_palindrome=true&contains_character=a

### 3️⃣ GET /strings/?query=... — Natural Language Query

Examples:

/strings/?query=all single word palindromic strings
/strings/?query=strings longer than 10 characters

### 4️⃣ GET /strings/<string_value>/ — Fetch details of a specific string

Example:

GET /strings/racecar/

### 5️⃣ DELETE /strings/<string_value>/ — Delete an analyzed string

Example:

DELETE /strings/racecar/


Response:

204 No Content

## 🧾 Example Natural Queries
Query	Parsed Filters
all single word palindromic strings	word_count=1, is_palindrome=true
strings longer than 10 characters	min_length=11
strings containing the letter z	contains_character=z
palindromic strings that contain the first vowel	is_palindrome=true, contains_character=a
⚡ Deployment on Railway
Required Files:

Procfile

runtime.txt

requirements.txt

.env

Example Procfile
web: python manage.py collectstatic --noinput && gunicorn string_analyser.wsgi

Example runtime.txt
python-3.12.6

Example requirements.txt
Django>=5.0
djangorestframework
gunicorn
whitenoise
python-dotenv
dj-database-url


Then push to GitHub and connect your repo to Railway.
Railway will detect the Django app automatically and build it.

## ✅ API Testing Tips

Use Postman Desktop Agent for localhost testing.

Set header:

Content-Type: application/json


Test locally:

http://127.0.0.1:8000/strings/


Test after deploy:

https://your-railway-url.up.railway.app/strings/

🧑‍💻 Author

Beatrice Mwangi
Backend Developer | Python & Django Enthusiast
🌐 GitHub: @Betty20000

###🚀 Backend Wizards Program — Stage 1

#### 💡 Exiting Bash or Virtual Environment

To exit Bash shell:

exit


or press
Ctrl + D

#### To deactivate your virtual environment:

deactivate
🚀 Built for the Backend Wizards Program

