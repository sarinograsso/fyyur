Fyyur
-----

## Introduction

This is Project 1 of the Udacity Full Stack Web Developer Nanodegree Program.

Fyyur is a musical venue and artist booking site that facilitates the discovery and bookings of shows between local performing artists and venues. This site lets you list new artists and venues, discover them, and list shows with artists as a venue owner.

The objective of the project is to build out the data models to power the API endpoints for the Fyyur site by connecting to a PostgreSQL database for storing, querying, and creating information about artists and venues on Fyyur.

## Tech Stack (Dependencies)

### 1. Backend Dependencies
Our tech stack will include the following:
 * **virtualenv** as a tool to create isolated Python environments
 * **SQLAlchemy ORM** to be our ORM library of choice
 * **PostgreSQL** as our database of choice
 * **Python3** and **Flask** as our server language and server framework
 * **Flask-Migrate** for creating and running schema migrations

### 2. Frontend Dependencies
You must have the **HTML**, **CSS**, and **Javascript** with [Bootstrap 3](https://getbootstrap.com/docs/3.4/customize/) for our website's frontend.

## How to setup the app locally
1. **Download the code from this repository**

2. **Initialize and activate a virtualenv using:**
```
python3 -m virtualenv env
source env/bin/activate
```
>**Note** - In Windows, the `env` does not have a `bin` directory. Therefore, you'd use the analogous command shown below:
```
source env/Scripts/activate
```

3. **Install the dependencies:**
```
pip3 install -r requirements.txt
```

4. **Create a PostgreSQL database and set the connection on the config.py file**
```
SQLALCHEMY_DATABASE_URI = 'postgresql://<username>:<password>@localhost:5432/<database_name>'
```

5. **Run the database migrations**
```
flask db upgrade
```

6. **Run the development server:**
```
python3 app.py
```

7. **Verify on the Browser**<br>
Navigate to project homepage [http://127.0.0.1:5000/](http://127.0.0.1:5000/) or [http://localhost:5000](http://localhost:5000)
