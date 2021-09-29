from typing import Tuple
from flask import Flask
from flask import render_template
from flask import request, url_for, redirect
import mariadb
import sys
import json

app = Flask(__name__)

# connection parameters
db_conn_params = {
    "host":"127.0.0.1",
    "port":3306,
    "user":"root",
    "password":"mariaDB",
    "database":"pi1_db"
}


try:
    conn = mariadb.connect(
#        host="127.0.0.1",
        host=db_conn_params["host"],
        port=3306,
        user="root",
        password="mariaDB",
        database="pi1_db"
        )
except mariadb.Error as e:
    print(f"Error connection to MariaDB Platform: {e}")
    sys.exit(1)
cursor = conn.cursor()


def db_insert_one(sql, data):
    try:
        conn = mariadb.connect(
            host=db_conn_params["host"],
            port=db_conn_params["port"],
            user=db_conn_params["user"],
            password=db_conn_params["password"],
            database=db_conn_params["database"]
            )
    except mariadb.Error as e:
        print(f"Error connection to MariaDB Platform: {e}")
        sys.exit(1)
    cursor = conn.cursor()
    cursor.execute(sql,data)
    conn.commit()
    #conn.close()



def db_insert(sql,dados):
    try:
        conn = mariadb.connect(
            host=db_conn_params["host"],
            port=db_conn_params["port"],
            user=db_conn_params["user"],
            password=db_conn_params["password"],
            database=db_conn_params["database"]
            )
    except mariadb.Error as e:
        print(f"Error connection to MariaDB Platform: {e}")
        sys.exit(1)
    cursor = conn.cursor()
    cursor.executemany(sql,dados)
    conn.commit()
    conn.close()




def db_cmd(sql):
    try:
        conn = mariadb.connect(
            host=db_conn_params["host"],
            port=db_conn_params["port"],
            user=db_conn_params["user"],
            password=db_conn_params["password"],
            database=db_conn_params["database"]
            )
    except mariadb.Error as e:
        print(f"Error connection to MariaDB Platform: {e}")
        sys.exit(1)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()




@app.route("/")
def index():
    sql = "SELECT * FROM users;"
    cursor.execute(sql)
    lista = cursor.fetchall()
    return render_template('index.html', lista=lista)


@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        nome = request.form['fname']
        curso = request.form['course']
        sql =  "INSERT INTO users (id, name, course) VALUES (?, ?, ?);"
        data = [(4, str(nome), str(curso))]
        db_insert(sql,data)
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route("/delete/<row>", methods=['GET', 'POST'])
def delete(row):
    if request.method == 'GET':
        sql = "DELETE FROM users WHERE id={};".format(row)
        db_cmd(sql)
    return redirect(url_for('index'))


@app.route("/edit/<row>", methods=['GET', 'POST'])
def edit(row):
    if request.method == 'GET':
        sql = "SELECT * FROM users WHERE id={};".format(row)
        cursor.execute(sql)
        lista = cursor.fetchall()
        return render_template('edit.html', lista=lista)
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
