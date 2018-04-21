from flask import Flask, render_template, json, jsonify, request, make_response
from flaskext.mysql import MySQL
from healthcheck import HealthCheck, EnvironmentDump

SERVER_PORT = 5002

DB_NAME = "raamatukogu"
DB_HOST = "localhost"
DB_USER = "root"
DB_PASS = ""

mysql = MySQL()
app = Flask(__name__)


health = HealthCheck(app, "/healthcheck")
envdump = EnvironmentDump(app, "/environment", include_os=True, include_python=True, include_process=False, include_config=False)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = DB_USER
app.config['MYSQL_DATABASE_PASSWORD'] = DB_PASS
app.config['MYSQL_DATABASE_DB'] = DB_NAME
app.config['MYSQL_DATABASE_HOST'] = DB_HOST


def mysql_is_available_and_has_tables():
    test_table1 = "SELECT * FROM " + DB_NAME + ".kataloog;"
    test_table2 = "SELECT * FROM " + DB_NAME + ".statistika;"

    test_proc = "CALL get_books();"

    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(test_table1)
        cursor.execute(test_table2)
        cursor.execute(test_proc)
    except:
        return False, "FAILURE"
    cursor.close()
    conn.close()
    return True, "OK"


health.add_check(mysql_is_available_and_has_tables)


def application_data():
    return {"developer": "Nikita Kovalenko",
            "git_repo": "https://github.com/nikkov96/raamatukogu"}


envdump.add_section("application", application_data)

mysql.init_app(app)


@app.route('/')
def main():
    return show_all()


@app.route("/all", methods=["GET"])
def show_all():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.callproc('get_books')
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template("index.html", data=data)
    except Exception as e:
        return str(e)


@app.route('/form/<id>')
def show_form(id):
    return render_template('form.html', kood=id)


@app.route('/order', methods=['POST', 'GET'])
def order():
    try:
        book_id = request.form['kood']
        nimi = request.form['nimi']
        email = request.form['email']
        telefon = str(request.form['telefon'])
        isikukood = str(request.form['isikukood'])

        if book_id and nimi and email and telefon and isikukood:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('add_order', (book_id, nimi, email, telefon, isikukood))
            data = cursor.fetchall()
            if len(data) is 0:
                conn.commit()
                cursor.close()
                conn.close()
                return json.dumps({'message': 'Order created successfully!'})
            else:
                cursor.close()
                conn.close()
                return json.dumps({'error': str(data[0])})
        else:
            return json.dumps({'error': 'Fill in all fields!'})

    except Exception as e:
        return json.dumps({'error': str(e)})


@app.route('/tagasta/<id>')
def tagasta(id):
    return render_template("tagasta.html", data=id)


@app.route('/tagasta', methods=['POST', 'GET'])
def finish():
    try:
        book_id = request.form['kood']
        telefon = str(request.form['telefon'])
        isikukood = str(request.form['isikukood'])

        if book_id and telefon and isikukood:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('finish_book', (book_id, telefon, isikukood))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                cursor.close()
                conn.close()
                return json.dumps({'message': 'Book returned successfully!'})
            else:
                cursor.close()
                conn.close()
                return json.dumps({'error': str(data[0])})
        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error': str(e)})


@app.route("/all/<search>", methods=["POST", "GET"])
def show_searched(search):
    try:
        searching = search
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.callproc('do_search', [str(searching)])
        data = cursor.fetchall()
        return render_template("index.html", data=(data))
    except:
        return show_all()


def start_server(port):
    app.run(port=port)


if __name__ == "__main__":
    start_server(port=SERVER_PORT)
