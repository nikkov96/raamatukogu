# Raamatukogu

Python 3.6 + Flask with MySQL

## Requirements:
  - MySQL
  - pip
    - flask
    - flask_mysql
    - healthcheck (On not-UNIX OS (Windows) need to change *os.uname()* to *os.name* in *healthcheck/\_\_init\_\_.py* in function *get_os()*)

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

### HEALTHCHECK
View healthcheck status
```
http://localhost:5002/healthcheck
```
View environment
```
http://localhost:5002/environment
```

### TESTING (test.py):
```
 python -m unittest discover -p test.py
```
