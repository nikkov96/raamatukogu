# Raamatukogu

Python 3.6 + Flask with MySQL

Requirements:
  - MySQL
  - pip
    - flask
    - flask_mysql

### HOW TO RUN:
1) in app.py set *SERVER_PORT*, *DB_NAME*, *DB_HOST*, *DB_USER*, *DB_PASS*
2) Create database, tables and procedures
```
python sql.py
```
3) Run the app
```
python app.py
```
4) Go to http://localhost:{SERVER_PORT}

### TESTING (test.py):
```
 python -m unittest discover -p test.py
```
