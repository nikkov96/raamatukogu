from flask import Flask
from flaskext.mysql import MySQL
from app import DB_USER, DB_PASS, DB_HOST, DB_NAME

mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = DB_USER
app.config['MYSQL_DATABASE_PASSWORD'] = DB_PASS
app.config['MYSQL_DATABASE_DB'] = ''
app.config['MYSQL_DATABASE_HOST'] = DB_HOST

mysql.init_app(app)


def get_queries(db):

    drop_db = "DROP DATABASE IF EXISTS " + db + ";"
    create_db = "CREATE DATABASE " + db + ";"
    create_kataloog = "CREATE TABLE " + db + ".kataloog( book_id int NOT NULL PRIMARY KEY, book_name varchar(255) NOT NULL, book_author varchar(100) NOT NULL, book_year int NOT NULL);"
    create_statistika = "CREATE TABLE " + db + ".statistika( laen_id int NOT NULL AUTO_INCREMENT PRIMARY KEY, book_id int NOT NULL, start_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, finish_date DATETIME DEFAULT NULL, laenaja_nimi varchar(100) NOT NULL, laenaja_email varchar(100) NOT NULL, laenaja_telefon VARCHAR(20) NOT NULL, laenaja_isikukood VARCHAR(20) NOT NULL, FOREIGN KEY (book_id) REFERENCES kataloog(book_id));"

    # SQL Procedures
    proc_add = """
    CREATE PROCEDURE """ + db + """.add_order (IN book int,IN nimi varchar(100),IN email varchar(100), IN telefon varchar(20), IN isikukood varchar(20))
    BEGIN
        INSERT INTO statistika(book_id,laenaja_nimi,laenaja_email,laenaja_telefon,laenaja_isikukood)
        VALUES (book,nimi,email,telefon,isikukood);
    END
    """

    proc_get = """
    CREATE PROCEDURE """ + db + """.get_books()
    BEGIN
        SELECT *
        FROM kataloog;
    END
    """

    proc_finish = """
    CREATE PROCEDURE """ + db + """.finish_book(IN book int, IN telefon varchar(20), IN isikukood varchar(20))
    BEGIN
    	UPDATE statistika
    	SET finish_date = CURRENT_TIMESTAMP
    	WHERE book_id = book AND laenaja_telefon = telefon AND laenaja_isikukood = isikukood AND finish_date IS NULL
    	LIMIT 1;
    END
    """

    proc_find = """
    CREATE PROCEDURE """ + db + """.do_search(IN s varchar(100))
    BEGIN
    	SELECT * FROM kataloog
    	WHERE book_name LIKE CONCAT('%', TRIM(s), '%') OR book_author LIKE CONCAT('%', TRIM(s), '%');
    END
    """

    # Queries to create sample data
    create_book1 = "INSERT INTO " + db + ".kataloog (book_id, book_name, book_author, book_year) VALUES (1, 'Book 1', 'Author 1', 1901);"
    create_book2 = "INSERT INTO " + db + ".kataloog (book_id, book_name, book_author, book_year) VALUES (2, 'Book 2', 'Author 2', 1902);"
    create_book3 = "INSERT INTO " + db + ".kataloog (book_id, book_name, book_author, book_year) VALUES (3, 'Book 3', 'Author 3', 1903);"
    create_book4 = "INSERT INTO " + db + ".kataloog (book_id, book_name, book_author, book_year) VALUES (4, 'Book 4', 'Author 4', 1904);"
    create_book5 = "INSERT INTO " + db + ".kataloog (book_id, book_name, book_author, book_year) VALUES (5, 'Book 5', 'Author 5', 1905);"

    firstly = [drop_db, create_db, create_kataloog, create_statistika]
    secondly = [create_book1, create_book2, create_book3, create_book4, create_book5]
    lastly = [proc_get, proc_add, proc_finish, proc_find]

    return firstly + secondly + lastly


def init_db():  # Creates DB, tables, sample data, procedures
    conn = mysql.connect()
    cursor = conn.cursor()
    for query in get_queries(DB_NAME):
        cursor.execute(query)
    conn.close()
    cursor.close()
    print("Successfully created database, tables and procedures")


if __name__ == '__main__':
    init_db()
