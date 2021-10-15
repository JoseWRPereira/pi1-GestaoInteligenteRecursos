from flask import Flask
from flask import render_template
from flask import request, url_for, redirect
import mariadb
import sys
import json


class Calendario:
    def __init__(self):
        self.data = ""
    def set(self, dt ):
        self.data = dt
    def get(self):
        return(self.data)

class Carrinho:
    def __init__(self):
        self.carrinho = ""
    def set(self, lista ):
        self.carrinho = lista
    def get(self):
        return(self.carrinho)

class Acesso:
    def __init__(self):
        self.uc = ''
        self.user = ''
        self.pwd = ''
    def set_uc(self, uc):
        self.uc = uc
    def set_user(self, user):
        self.user = user
    def set_pwd(self,pwd):
        self.pwd = pwd
    def get_uc(self):
        return(self.uc)
    def get_user(self):
        return(self.user)
    def get_pwd(self):
        return(self.pwd)

class LoginAcesso:
    def __init__(self):
        self.msg = ""
        self.campo = ""
        self.sql = ""
    def set(self, m,c,s):
        self.msg = m
        self.campo = c
        self.sql = s
    def get_msg(self):
        return(self.msg)
    def get_campo(self):
        return(self.campo)
    def get_sql(self):
        return(self.sql)



app = Flask(__name__)

car = Carrinho()
cal = Calendario()
acesso = Acesso()
loginAcesso = LoginAcesso()

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
    sql = "CREATE TABLE IF NOT EXISTS pi1_db.disciplina( codigo varchar(6) not null, nome varchar(50) not null, primary key(codigo));"
    db_cmd(sql)
    sql = "CREATE TABLE IF NOT EXISTS pi1_db.usuario( nif INT NOT NULL, nome VARCHAR(50) NOT NULL, disciplina VARCHAR(6), admissao VARCHAR(20), PRIMARY KEY(nif), FOREIGN KEY(disciplina) REFERENCES disciplina(codigo) );"
    db_cmd(sql)
    sql = "CREATE TABLE IF NOT EXISTS pi1_db.equipamento( np INT NOT NULL, nome VARCHAR(50) NOT NULL, carrinho INT, descricao VARCHAR(50), adquirido_em DATE, ultima_manutencao_em DATE, status VARCHAR(20), PRIMARY KEY(np));"
    db_cmd(sql)
    sql = "CREATE TABLE IF NOT EXISTS pi1_db.carrinho( id INT NOT NULL, nome VARCHAR(50) NOT NULL, qtd_equipamentos INT, status VARCHAR(50), obs VARCHAR(50), PRIMARY KEY(id));"
    db_cmd(sql)
    sql = "CREATE TABLE IF NOT EXISTS pi1_db.reserva( id INT NOT NULL AUTO_INCREMENT, data DATE, carrinho_id INT, usuario_id INT, PRIMARY KEY(id), FOREIGN KEY(carrinho_id) REFERENCES carrinho(id), FOREIGN KEY(usuario_id) REFERENCES usuario(nif) );"
    db_cmd(sql)

    loginAcesso.set("Escolha a unidade curricular:","disciplina","SELECT codigo,nome FROM disciplina;")
    return redirect(url_for('login'))


@app.route("/login")
def login():
    lista = db_cmd(loginAcesso.get_sql())
    return render_template('login.html', msg=loginAcesso.get_msg(), campo=loginAcesso.get_campo(), lista=lista )

@app.route("/login/disciplina/<uc>")
def login_disciplina(uc):
    acesso.set_uc( uc )
    loginAcesso.set("Escolha o usuário de acesso:","usuario","SELECT nif,nome FROM usuario WHERE disciplina='{}';".format(acesso.get_uc()))
    return redirect(url_for('login'))

@app.route("/login/usuario/<nif>")
def login_usuario(nif):
    acesso.set_user(nif)
    return redirect(url_for('loginsenha'))

@app.route("/loginsenha", methods=['GET','POST'])
def loginsenha():
    if request.method == 'POST':
        acesso.set_pwd(request.form['pwd'])
        return redirect(url_for('manager'))
    return render_template('loginsenha.html');



@app.route("/manager", methods=['GET', 'POST'])
def manager():
    sql = "SELECT * FROM reserva WHERE data=CURDATE();"
    lista = db_cmd(sql)
    imp = ""
    if request.method == 'POST':
        cal.set(request.form['calendario'])
        sql =  "SELECT * FROM reserva WHERE data='{}' ORDER BY carrinho_id;".format( cal.get() )
        lista = db_cmd(sql)
        sql = "SELECT id,nome FROM carrinho WHERE id NOT IN (SELECT carrinho_id FROM reserva where data='{}' ORDER BY carrinho_id);".format(cal.get())
        car.set( db_cmd(sql) )
    return render_template('manager.html', lista=lista, car=car.get(), cal=cal.get(), imp=imp )

@app.route("/manager/<car_id>", methods=['GET', 'POST'])
def manager_car(car_id):
    sql =  "INSERT INTO reserva (data, carrinho_id, usuario_id) VALUES ('{}', '{}', '{}');".format(cal.get(), car_id, acesso.get_user())
    db_cmd(sql)
    return redirect(url_for('manager'))
    



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
    # sql = "CREATE TABLE IF NOT EXISTS pi1_db.disciplina( codigo varchar(5) not null, nome varchar(50) not null, primary key(codigo));"
    # db_cmd(sql)
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
    # sql = "CREATE TABLE IF NOT EXISTS pi1_db.usuario( nif INT NOT NULL, nome VARCHAR(50) NOT NULL, disciplina VARCHAR(30), admissao VARCHAR(20), PRIMARY KEY(nif), FOREIGN KEY(disciplina) REFERENCES disciplina(codigo) );"
    # db_cmd(sql)
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
    # sql = "CREATE TABLE IF NOT EXISTS pi1_db.equipamento( np INT NOT NULL, nome VARCHAR(50) NOT NULL, carrinho INT, descricao VARCHAR(50), adquirido_em DATE, ultima_manutencao_em DATE, status VARCHAR(20), PRIMARY KEY(np));"
    # db_cmd(sql)
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
    # sql = "CREATE TABLE IF NOT EXISTS pi1_db.carrinho( id INT NOT NULL, nome VARCHAR(50) NOT NULL, qtd_equipamentos INT, status VARCHAR(50), obs VARCHAR(50), PRIMARY KEY(id));"
    # db_cmd(sql)
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
###      PI1_DB Reservas
###############################################################################

@app.route("/tb_reservas", methods=['GET', 'POST'])
def tb_reservas():
    # sql = "CREATE TABLE IF NOT EXISTS pi1_db.reserva( id INT NOT NULL AUTO_INCREMENT, data DATE, carrinho_id INT, usuario_id INT, PRIMARY KEY(id), FOREIGN KEY(carrinho_id) REFERENCES carrinho(id), FOREIGN KEY(usuario_id) REFERENCES usuario(nif) );"
    # db_cmd(sql)
    if request.method == 'POST':
        cal_ = request.form['calendario']
        car_ = request.form['carrinho']
        usr_ = request.form['usuario']
        sql =  "INSERT INTO reserva (data, carrinho_id, usuario_id) VALUES ('{}','{}','{}');".format(str(cal_), str(car_), str(usr_))
        db_cmd(sql)
        return redirect(url_for('tb_reservas'))
    sql = "SELECT * FROM carrinho;"
    car = db_cmd(sql)
    sql = "SELECT * FROM usuario;"
    usr = db_cmd(sql)
    sql = "SELECT * FROM reserva;"
    lista = db_cmd(sql)
    return render_template('tb_reservas.html', lista=lista, car=car, usr=usr )

# @app.route("/addreserva/<id>", methods=['GET', 'POST'])
# def addreserva(id):
#     sql = "DELETE FROM carrinho WHERE id='{}';".format(id)
#     db_cmd(sql)
#     return redirect(url_for('tb_carrinhos'))

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
