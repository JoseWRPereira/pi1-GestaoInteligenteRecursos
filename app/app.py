from flask import Flask
from flask import render_template
from flask import request, url_for, redirect
from flask.templating import render_template_string
import mariadb
import sys
# import json
from datetime import datetime, date, timedelta



###############################################################################
######################################## Conexão com o Banco de Dados - MariaDB
###############################################################################
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


###############################################################################
####################################################################### Classes
###############################################################################
class Disciplina:
    def __init__(self):
        self.codigo = ""
        self.nome = ""
    def set_codigo(self, code):
        self.codigo = code
    def set_nome(self, name):
        self.nome = name
    def get_codigo(self):
        return(self.codigo)
    def get_nome(self):
        return(self.nome)

class Usuario:
    def __init__(self):
        self.nif = 0
        self.nome = ""
        self.disciplina = ""
    def set_nif(self, nif):
        self.nif = nif
    def set_nome(self,nome):
        self.nome = nome
    def set_disciplina(self,disciplina):
        self.disciplina = disciplina
    def get_nif(self):
        return(self.nif)
    def get_nome(self):
        return(self.nome)
    def get_disciplina(self):
        return(self.disciplina)

class Carrinho:
    def _init__(self):
        self.id=0
        self.nome = ""
        self.qtd_equipamentos = 0
    def set_id(self, id):
        self.id = id
    def set_nome(self, nome):
        self.nome = nome
    def set_qtd_equipamentos(self, qtd):
        self.qtd_equipamentos = qtd
    def get_id(self):
        return(self.id)
    def get_nome(self):
        return(self.nome)
    def get_qtd_equipamentos(self):
        return(self.qtd_equipamentos)
        
class Equipamento:# np, nome, carrinho, descricao, adquirido_em, status
    def __init__(self):
        self.np = 0
        self.nome = ""
        self.carrinho = 0
        self.descricao = ""
        self.adquisido_em = 0
        self.status = ""
    def set_np(self,np):
        self.np = np
    def set_nome(self,nome):
        self.nome = nome
    def set_carrinho(self,carrinho):
        self.carrinho = carrinho
    def get_np(self):
        return(self.np)
    def get_nome(self):
        return(self.nome)
    def get_carrinho(self):
        return(self.carrinho)


class Reserva:#( id, data, carrinho_id, usuario_id
    def __init__(self):
        self.data = 0
        self.carrinho_id = 0
        self.usuario_id = 0
    def set_data(self,data):
        self.data = data
    def set_carrinho_id(self,carrinho):
        self.carrinho_id = carrinho
    def set_usuario_id(self,usuario):
        self.usuario_id = usuario
    def get_data(self):
        return(self.data)
    def get_carrinho_id(self):
        return(self.carrinho_id)
    def get_usuario_id(self):
        return(self.usuario_id)
    

class Calendario:
    def __init__(self):
        self.data = date.today()
        self.delta = 0
    def set_delta(self, delta):
        self.delta = delta
    def get_delta(self):
        return(self.delta)
    def get_data(self):
        return(self.data + timedelta(days = self.delta))

###############################################################################
################################################################ Instanciamento
###############################################################################
app = Flask(__name__)
disciplina = Disciplina()
usuario = Usuario()
carrinho = Carrinho()
equipamento = Equipamento()
reserva = Reserva()
calendario = Calendario()




###############################################################################
######################################################################### index
###############################################################################

@app.route("/")
def index():
    return render_template('index.html')





###############################################################################
################################################################# create tables
###############################################################################

@app.route("/createtables")
def createtables():
    sql = "CREATE TABLE IF NOT EXISTS pi1_db.disciplina( codigo varchar(6) not null, nome varchar(50) not null, primary key(codigo));"
    db_cmd(sql)
    sql = "CREATE TABLE IF NOT EXISTS pi1_db.usuario( nif INT NOT NULL, nome VARCHAR(50) NOT NULL, disciplina VARCHAR(6), PRIMARY KEY(nif), FOREIGN KEY(disciplina) REFERENCES disciplina(codigo) );"
    db_cmd(sql)
    sql = "CREATE TABLE IF NOT EXISTS pi1_db.carrinho( id INT NOT NULL, nome VARCHAR(16) NOT NULL, qtd_equipamentos INT, PRIMARY KEY(id));"
    db_cmd(sql)
    sql = "CREATE TABLE IF NOT EXISTS pi1_db.equipamento( np INT NOT NULL, nome VARCHAR(20) NOT NULL, carrinho INT, descricao VARCHAR(50), adquirido_em DATE, status VARCHAR(16), PRIMARY KEY(np));"
    db_cmd(sql)
    sql = "CREATE TABLE IF NOT EXISTS pi1_db.reserva( id INT NOT NULL AUTO_INCREMENT, data DATE, carrinho_id INT, usuario_id INT, PRIMARY KEY(id), FOREIGN KEY(carrinho_id) REFERENCES carrinho(id), FOREIGN KEY(usuario_id) REFERENCES usuario(nif) );"
    db_cmd(sql)
    return redirect(url_for('main'))





###############################################################################
########################################################################## main
###############################################################################

@app.route("/main")
def main():
    data = calendario.get_data()
    sql = "SELECT * FROM reserva WHERE data='{}';".format(data)
    lista = db_cmd(sql)
    return render_template('main.html', lista=lista, data=data  )

@app.route("/main/datadec", methods=['GET','POST'])
def maindatadec():
    calendario.set_delta( calendario.get_delta()-1 )
    return redirect(url_for('main'))


@app.route("/main/datainc", methods=['GET','POST'])
def maindatainc():
    calendario.set_delta( calendario.get_delta()+1 )
    return redirect(url_for('main'))




@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/agendar")
def agendar():
    return render_template('agendar.html')


###############################################################################
##################################################################### Gerenciar
###############################################################################

@app.route("/gerenciar")
def gerenciar():
    return render_template('gerenciar.html')



###############################################################################
######################################################### Gerenciar disciplinas
################################################################ (codigo), nome
###############################################################################
@app.route("/gerenciar/disciplinas", methods=['GET','POST'])
def gerenciardisciplinas(): 
    if request.method == 'POST':
        disciplina.set_codigo(request.form['disciplinaCodigo'])
        disciplina.set_nome(request.form['disciplinaNome'])
        if disciplina.get_codigo != ' ':
            return redirect(url_for('gerenciardisciplinasadd'))
    else:
        sql = "SELECT * FROM disciplina;"
        lista = db_cmd(sql)
        return render_template('gerenciar_disciplinas.html', lista=lista  )

@app.route("/gerenciar/disciplinas/add")
def gerenciardisciplinasadd():  
    sql =  "INSERT INTO disciplina (codigo, nome) VALUES ('{}', '{}');".format(str(disciplina.get_codigo()), str(disciplina.get_nome()))
    db_cmd(sql)
    return redirect(url_for('gerenciardisciplinas'))

@app.route("/gerenciar/disciplinas/del/<codigo>", methods=['GET', 'POST'])
def gerenciardisciplinasdel(codigo):
    sql = "DELETE FROM disciplina WHERE codigo='{}';".format(codigo)
    db_cmd(sql)
    return redirect(url_for('gerenciardisciplinas'))





###############################################################################
############################################################ Gerenciar usuarios
################################# (nif), nome, [disciplina]->disciplina(codigo)
###############################################################################

@app.route("/gerenciar/usuarios", methods=['GET','POST'])
def gerenciarusuarios():
    if request.method == 'POST':
        usuario.set_nif(request.form['usuarioNIF'])
        usuario.set_nome(request.form['usuarioNome'])
        usuario.set_disciplina(request.form['usuarioDisciplina'])
        return redirect(url_for('gerenciarusuariosadd'))
    else:
        sql = "SELECT * FROM disciplina;"
        discip = db_cmd(sql)
        sql = "SELECT * FROM usuario;"
        lista = db_cmd(sql)
        return render_template('gerenciar_usuarios.html', lista=lista, discip=discip )

@app.route("/gerenciar/usuarios/add")
def gerenciarusuariosadd():
    sql =  "INSERT INTO usuario (nif, nome, disciplina) VALUES ('{}','{}','{}');".format(str(usuario.get_nif()), str(usuario.get_nome()), str(usuario.get_disciplina()) )
    db_cmd(sql)
    return redirect(url_for('gerenciarusuarios'))

@app.route("/gerenciar/usuarios/del/<codigo>", methods=['GET', 'POST'])
def gerenciarusuariosdel(codigo):
    sql = "DELETE FROM usuario WHERE nif='{}';".format(codigo)
    db_cmd(sql)
    return redirect(url_for('gerenciarusuarios'))





###############################################################################
########################################################### Gerenciar carrinhos
################################################## (id), nome, qtd_equipamentos
###############################################################################
@app.route("/gerenciar/carrinhos", methods=['GET','POST'])
def gerenciarcarrinhos():
    if request.method == 'POST':
        carrinho.set_id(request.form['carrinhoId'])
        carrinho.set_nome(request.form['carrinhoNome'])
        return redirect(url_for('gerenciarcarrinhosadd'))
    else:
        sql = "SELECT * FROM carrinho;"
        lista = db_cmd(sql)
        return render_template('gerenciar_carrinhos.html', lista=lista )

@app.route("/gerenciar/carrinhos/add")
def gerenciarcarrinhosadd():
    sql =  "INSERT INTO carrinho (id, nome) VALUES ('{}','{}');".format(str(carrinho.get_id() ), str(carrinho.get_nome()))
    db_cmd(sql)
    return redirect(url_for('gerenciarcarrinhos'))

@app.route("/gerenciar/carrinhos/del/<id>", methods=['GET', 'POST'])
def gerenciarcarrinhosdel(id):
    sql = "DELETE FROM carrinho WHERE id='{}';".format(id)
    db_cmd(sql)
    return redirect(url_for('gerenciarcarrinhos'))





###############################################################################
######################################################## Gerenciar equipamentos
######################### (np), nome, carrinho, descricao, adquirido_em, status
###############################################################################
@app.route("/gerenciar/equipamentos", methods=['GET','POST'])
def gerenciarequipamentos():
    if request.method == 'POST':
        equipamento.set_np(request.form['equipNumPatr'])
        equipamento.set_nome(request.form['equipNome'])
        equipamento.set_carrinho(request.form['equipCarrinho'])
        return redirect(url_for('gerenciarequipamentosadd'))
    else:
        sql = "SELECT * FROM carrinho;"
        carrinho = db_cmd(sql)
        sql = "SELECT * FROM equipamento;"
        lista = db_cmd(sql)
        return render_template('gerenciar_equipamentos.html', lista=lista, carrinho=carrinho)

@app.route("/gerenciar/equipamentos/add")
def gerenciarequipamentosadd():
    sql =  "INSERT INTO equipamento (np, nome, carrinho) VALUES ('{}','{}','{}');".format(str(equipamento.get_np()), str(equipamento.get_nome()), str(equipamento.get_carrinho()) )
    db_cmd(sql)
    return redirect(url_for('gerenciarequipamentos'))

@app.route("/gerenciar/equipamentos/del/<id>", methods=['GET', 'POST'])
def gerenciarequipamentosdel(id):
    sql = "DELETE FROM equipamento WHERE np='{}';".format(id)
    db_cmd(sql)
    return redirect(url_for('gerenciarequipamentos'))





###############################################################################
############################################################ Gerenciar reservas
############### (id), data, carrinho_id->carrinho(id), usuario_id->usuario(nif)
###############################################################################
@app.route("/gerenciar/reservas", methods=['GET','POST'])
def gerenciarreservas():
    if request.method == 'POST':
        reserva.set_data(request.form['calendario'])
        reserva.set_carrinho_id(request.form['carrinho'])
        reserva.set_usuario_id(request.form['usuario'])
        return redirect(url_for('gerenciarreservasadd'))
    else:
        sql = "SELECT id,nome FROM carrinho;"
        carrinho = db_cmd(sql)
        sql = "SELECT nif,nome FROM usuario;"
        usuario = db_cmd(sql)
        sql = "SELECT * FROM reserva;"
        lista = db_cmd(sql)
        return render_template('gerenciar_reservas.html', lista=lista, carrinho=carrinho, usuario=usuario)

@app.route("/gerenciar/reservas/add")
def gerenciarreservasadd():
    sql =  "INSERT INTO reserva (data, carrinho_id, usuario_id) VALUES ('{}','{}','{}');".format(str(reserva.get_data()), str(reserva.get_carrinho_id()), str(reserva.get_usuario_id()) )
    db_cmd(sql)
    return redirect(url_for('gerenciarreservas'))

@app.route("/gerenciar/reservas/del/<id>", methods=['GET', 'POST'])
def gerenciarreservasdel(id):
    sql = "DELETE FROM reserva WHERE id='{}';".format(id)
    db_cmd(sql)
    return redirect(url_for('gerenciarreservas'))



###############################################################################
######################################################## PI1_DB DROP ALL TABLES
###############################################################################
@app.route("/dropalltables")
def dropalltables():
    sql = "DROP TABLE IF EXISTS reserva;"
    db_cmd(sql)
    sql = "DROP TABLE IF EXISTS equipamento;"
    db_cmd(sql)
    sql = "DROP TABLE IF EXISTS carrinho;"
    db_cmd(sql)
    sql = "DROP TABLE IF EXISTS usuario;"
    db_cmd(sql)
    sql = "DROP TABLE IF EXISTS disciplina;"
    db_cmd(sql)
    return redirect(url_for('createtables'))

###############################################################################
###############################################################################





if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

###############################################################################
###############################################################################
###############################################################################