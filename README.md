# Neusler CMS

Neusler is a content management system for publishers.

## Setup

Depends on

-   Python 3.9
-   Postgresql
-   Django 3.2.x

### Create database

In psql console run the following:

```sql
CREATE USER wagu WITH PASSWORD 'password';
CREATE DATABASE neuslerdb OWNER wagu;
```

### Clone and load data

```sh
git clone git@github.com:neumeral/neusler-lite.git neusler
cd neusler

# Create python virtual env
python3.9 -m venv venv
source venv/bin/activate

make dev #
```

### Run the server

```sh
python manage.py runserver
```

The server will be running at [http://localhost:8000](http://localhost:8000).

### Demo user credentials

-   username: admin password: password
-   username: john password: password
-   username: jane password: password

## Credits

Theme based on (nauvalazhar/Magz](https://github.com/nauvalazhar/Magz)
Licensed under the MIT License.
