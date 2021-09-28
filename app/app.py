from flask import Flask
from flask import render_template
from flask import request, url_for, redirect
import mariadb
import sys

app = Flask(__name__)


try:
    conn = mariadb.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="mariaDB",
        database="pi1_db"
        )
except mariadb.Error as e:
    print(f"Error connection to MariaDB Platform: {e}")
    sys.exit(1)
cursor = conn.cursor()



@app.route("/")
def index():
    cursor.execute("SELECT * FROM users;")
    lista = cursor.fetchall()
    return render_template('index.html', lista=lista)


@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        return redirect( url_for('index'))
    return render_template('add.html')



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)






# config_DB = {
#      'host':'127.0.0.1',
#      'port':3306,
#      'user':'root',
#      'password':'mariaDB',
#      'database':'pi1_db'
#  }


# try:
#     conn = mariadb.connect(
#         user="root",
#         password="mariaDB",
#         host="127.0.0.1",
#         port=3306,
#         database="pi1_db"
#         )
# except mariadb.Error as e:
#     print(f"Error connection to MariaDB Platform: {e}")
#     sys.exit(1)
# cursor = conn.cursor()

# def index():
#     conn = mariadb.connect(**config_DB)
#     cur = conn.cursor()
#     cur.execute("SELECT * from users;")

#     row_headers = [x[0] for x in cur.description]
#     rv = cur.fetchall()
#     json_data = []
#     for result in rv:
#         json_data.append(dict(zip(row_headers,result)))
#     return json.dumps(json_data)
#     # cursor.execute("SELECT * from users;", (usuarios))
#     # return render_template('index.html', usuarios=usuarios)

# conn = mariadb.connect(
#     host='127.0.0.1',
#     port=3306,
#     user='root',
#     password='mariaDB',
#     database='pi1_db'
# )

# cur = conn.cursor()

