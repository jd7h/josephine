# josephine
Book catalogue system in Python/Django.

## Etymology
josephine is named after Jo March, my favorite bookworm, from the novel Little Women by Louisa Alcott. 

## Setup (Linux)

Installation prerequisites: git, python, sqlite3

1. Cloning the repo:
```
git clone https://github.com/jd7h/josephine.git
cd josephine
```
2. Create a virtual environment and install dependencies:
```
cd josephine
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
3. Set up configfile, sqlite3 database and admin account
```
cp josephine/settings.example.py josephine/settings.py
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```
And follow the steps to create a superuser.

4. Start the Django server
```
python manage.py runserver
```
Point your browser at http://127.0.0.1:8000/admin and log in with your superuser account to view the admin panel.
Josephine is not ready to be used in production in any way.

## Inspiration
This project was inspired by GoodReads (owned by Amazon, not self-hosted), LibraryThing (not intuitive, not self-hosted), and https://books.hansdezwart.nl (PHP, not opensource). 
