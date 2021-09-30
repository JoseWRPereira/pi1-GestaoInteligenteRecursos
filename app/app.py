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



def db_cmd(sql):
    select = sql.count('SELECT') + sql.count('select')
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
    if select > 0:
        lista = cursor.fetchall()
    conn.commit()
    conn.close()
    if select > 0:
        return lista


@app.route("/")
def index():
    sql = "SELECT * FROM users;"
    lista = db_cmd(sql)
    return render_template('index.html', lista=lista)


@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        nome = request.form['addname']
        curso = request.form['addcourse']
        sql =  "INSERT INTO users (name, course) VALUES ('{}', '{}');".format(str(nome), str(curso))
        db_cmd(sql)
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route("/delete/<row>", methods=['GET', 'POST'])
def delete(row):
    sql = "DELETE FROM users WHERE id={};".format(row)
    db_cmd(sql)
    return redirect(url_for('index'))


@app.route("/edit/<id>", methods=['GET', 'POST'])
def edit(id):
    if request.method == 'GET':
        sql = "SELECT * FROM users WHERE id={};".format(id)
        lista = db_cmd(sql)
        return render_template('edit.html', usuario=lista)
    if request.method == 'POST':
        nome = request.form['editname']
        curso = request.form['editcourse']
        sql = "UPDATE users SET name='{}', course='{}' WHERE id={};".format(nome,curso, id)
        db_cmd(sql)
        return redirect(url_for('index'))


@app.route("/reset")
def reset():
    sql = "DROP TABLE IF EXISTS users;"
    db_cmd(sql)
    sql = "CREATE TABLE users ( id int not null AUTO_INCREMENT, name varchar(50) not null, course varchar(5) not null, primary key (id) );"
    db_cmd(sql)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
