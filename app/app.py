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




###############################################################################
###      PI1_DB Disciplinas
###############################################################################

@app.route("/tb_disciplinas", methods=['GET', 'POST'])
def tb_disciplinas():
    sql = "CREATE TABLE IF NOT EXISTS pi1_db.disciplina( codigo varchar(5) not null, nome varchar(50) not null, primary key(codigo));"
    db_cmd(sql)
    editar = ['','']
    if request.method == 'POST':
        codigo = request.form['disciplinaCodigo']
        nome = request.form['disciplinaNome']
        sql =  "INSERT INTO disciplina (codigo, nome) VALUES ('{}', '{}');".format(str(codigo), str(nome))
        db_cmd(sql)
        return redirect(url_for('tb_disciplinas'))
    sql = "SELECT * FROM disciplina;"
    lista = db_cmd(sql)
    return render_template('tb_disciplinas.html', lista=lista, editar=editar)

@app.route("/deldisciplina/<codigo>", methods=['GET', 'POST'])
def deldisciplina(codigo):
    sql = "DELETE FROM disciplina WHERE codigo='{}';".format(codigo)
    db_cmd(sql)
    return redirect(url_for('tb_disciplinas'))



###############################################################################
###      PI1_DB Usuarios
###############################################################################

@app.route("/tb_usuarios", methods=['GET', 'POST'])
def tb_usuarios():
    sql = "CREATE TABLE IF NOT EXISTS pi1_db.usuario( nif INT NOT NULL, nome VARCHAR(50) NOT NULL, disciplina VARCHAR(30), admissao VARCHAR(20), PRIMARY KEY(nif), FOREIGN KEY(disciplina) REFERENCES disciplina(codigo) );"
    db_cmd(sql)
    editar = ['','']
    sql = "SELECT * FROM disciplina;"
    ucs = db_cmd(sql)
    if request.method == 'POST':
        nif = request.form['usuarioNIF']
        nome = request.form['usuarioNome']
        disciplina = request.form['usuarioDisciplina']
        admissao = request.form['usuarioAdmissao']
        sql =  "INSERT INTO usuario (nif, nome, disciplina, admissao) VALUES ('{}','{}', '{}','{}');".format(str(nif), str(nome), str(disciplina), str(admissao) )
        db_cmd(sql)
        return redirect(url_for('tb_usuarios'))
    sql = "SELECT * FROM usuario;"
    lista = db_cmd(sql)
    return render_template('tb_usuarios.html', lista=lista, editar=editar, ucs=ucs)

@app.route("/delusuario/<nif>", methods=['GET', 'POST'])
def delusuario(nif):
    sql = "DELETE FROM usuario WHERE codigo='{}';".format(nif)
    db_cmd(sql)
    return redirect(url_for('tb_usuarios'))




###############################################################################
###      PI1_DB Equipamentos
###############################################################################

@app.route("/tb_equipamentos", methods=['GET', 'POST'])
def tb_equipamentos():
    sql = "CREATE TABLE IF NOT EXISTS pi1_db.equipamento( np INT NOT NULL, nome VARCHAR(50) NOT NULL, carrinho INT, descricao VARCHAR(50), adquirido_em VARCHAR(10), ultima_manutencao_em VARCHAR(10), status VARCHAR(20), PRIMARY KEY(np));"
    db_cmd(sql)
    editar = ['','']
    if request.method == 'POST':
        np = request.form['equipNumPatr']
        nome = request.form['equipNome']
        descricao = request.form['equipDescricao']
        aquisicao = request.form['equipAquisicao']
        manutencao = request.form['equipUltimaManut']
        status = request.form['equipStatus']
        sql =  "INSERT INTO equipamento (np, nome, descricao, adquirido_em, ultima_manutencao_em, status) VALUES ('{}','{}','{}','{}','{}','{}');".format(str(np), str(nome), str(descricao), str(aquisicao), str(manutencao), str(status) )
        db_cmd(sql)
        return redirect(url_for('tb_equipamentos'))
    sql = "SELECT * FROM equipamento;"
    lista = db_cmd(sql)
    return render_template('tb_equipamentos.html', lista=lista, editar=editar)

@app.route("/delequipamento/<np>", methods=['GET', 'POST'])
def delequipamento(np):
    sql = "DELETE FROM equipamento WHERE np='{}';".format(np)
    db_cmd(sql)
    return redirect(url_for('tb_equipamentos'))



###############################################################################
###      PI1_DB Carrinhos
###############################################################################

@app.route("/tb_carrinhos", methods=['GET', 'POST'])
def tb_carrinhos():
    sql = "CREATE TABLE IF NOT EXISTS pi1_db.carrinho( id INT NOT NULL, nome VARCHAR(50) NOT NULL, qtdEquipamentos INT, status VARCHAR(50), obs VARCHAR(50), PRIMARY KEY(id));"
    db_cmd(sql)
    editar = ['','']
    if request.method == 'POST':
        id = request.form['carrinhoId']
        nome = request.form['carrinhoNome']
        qtdEquipamentos = request.form['carrinhoQtdEquip']
        status = request.form['carrinhoStatus']
        obs = request.form['carrinhoObs']
        sql =  "INSERT INTO carrinho (id, nome, qtdEquipamentos, status, obs) VALUES ('{}','{}','{}','{}','{}');".format(str(id), str(nome), str(qtdEquipamentos), str(status), str(obs) )
        db_cmd(sql)
        return redirect(url_for('tb_carrinhos'))
    sql = "SELECT * FROM carrinho;"
    lista = db_cmd(sql)
    return render_template('tb_carrinhos.html', lista=lista, editar=editar)

@app.route("/delcarrinho/<id>", methods=['GET', 'POST'])
def delcarrinho(id):
    sql = "DELETE FROM carrinho WHERE id='{}';".format(id)
    db_cmd(sql)
    return redirect(url_for('tb_carrinhos'))


###############################################################################
###      PI1_DB DROP ALL TABLES
###############################################################################
@app.route("/dropalltables")
def dropalltables():
    sql = "DROP TABLE IF EXISTS usuario;"
    db_cmd(sql)
    sql = "DROP TABLE IF EXISTS equipamento;"
    db_cmd(sql)
    sql = "DROP TABLE IF EXISTS disciplina;"
    db_cmd(sql)
    sql = "DROP TABLE IF EXISTS carrinho;"
    db_cmd(sql)
    return redirect(url_for('index'))

###############################################################################
###############################################################################
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
