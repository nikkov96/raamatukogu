# Raamatukogu

Python 3.6 + Flask with MySQL

## Requirements:
  - MySQL
  - pip
    - flask
    - flask_mysql
    - healthcheck (On not-UNIX OS (such as Windows) change *os.uname()* to *os.name* or even better to *platform.uname()* with *import platform* in *healthcheck/\_\_init\_\_.py* in function *get_os()*)
      - six

### HOW TO RUN:
1) in **app.py** configure:

* *SERVER_PORT* (default=5002)
* *DB_NAME* (default=raamatukogu) 
  * *[**WARNING**] Database will be deleted if exists and created again with the required tables*
* *DB_HOST* (default=localhost)
* *DB_USER* (default=root)
* *DB_PASS* (default='')
  
  
  
2) Create database, tables and procedures
```python
python sql.py
```
3) Run the app
```python
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
```python
 python -m unittest discover -p test.py
```
