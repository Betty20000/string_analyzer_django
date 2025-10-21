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

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Betty20000/django-string-analyzer.git
cd django-string-analyzer
