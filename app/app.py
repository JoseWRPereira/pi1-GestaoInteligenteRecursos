from flask import Flask
from flask import render_template
from flask import request, url_for, redirect
from flask.templating import render_template_string
import mariadb
import sys
# import json


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
    def get_nif(self, nif):
        self.nif = nif
    def get_nome(self,nome):
        self.nome = nome
    def get_disciplina(self,disciplina):
        self.disciplina = disciplina

class Carrinho:
    def _init__(self):
        self.id=0
        self.nome = ""
        self.qtd_equipamentos
    def set_id(self, id):
        self.id = id
    def set_nome(self, nome):
        self.nome = nome
    def set_qtd_equipamentos(self, qtd):
        self.qtd_equipamentos = qtd
    def get_id(self, id):
        return(self.id)
    def get_nome(self, nome):
        return(self.nome)
    def get_qtd_equipamentos(self, qtd):
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
    def get_np(self,np):
        return(self.np)
    def get_nome(self,nome):
        return(self.nome)
    def get_carrinho(self,carrinho):
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
    def get_data(self,data):
        return(self.data)
    def get_carrinho_id(self,carrinho):
        return(self.carrinho_id)
    def get_usuario_id(self,usuario):
        return(self.usuario_id)
    




###############################################################################
################################################################ Instanciamento
###############################################################################
app = Flask(__name__)
disciplina = Disciplina()
usuario = Usuario()
carrinho = Carrinho()
equipamento = Equipamento()
reserva = Reserva()





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
    # sql = "CREATE TABLE IF NOT EXISTS pi1_db.disciplina( codigo varchar(6) not null, nome varchar(50) not null, primary key(codigo));"
    # db_cmd(sql)
    # sql = "CREATE TABLE IF NOT EXISTS pi1_db.usuario( nif INT NOT NULL, nome VARCHAR(50) NOT NULL, disciplina VARCHAR(6), PRIMARY KEY(nif), FOREIGN KEY(disciplina) REFERENCES disciplina(codigo) );"
    # db_cmd(sql)
    # sql = "CREATE TABLE IF NOT EXISTS pi1_db.carrinho( id INT NOT NULL, nome VARCHAR(16) NOT NULL, qtd_equipamentos INT, PRIMARY KEY(id));"
    # db_cmd(sql)
    # sql = "CREATE TABLE IF NOT EXISTS pi1_db.equipamento( np INT NOT NULL, nome VARCHAR(20) NOT NULL, carrinho INT, descricao VARCHAR(50), adquirido_em DATE, status VARCHAR(16), PRIMARY KEY(np));"
    # db_cmd(sql)
    # sql = "CREATE TABLE IF NOT EXISTS pi1_db.reserva( id INT NOT NULL AUTO_INCREMENT, data DATE, carrinho_id INT, usuario_id INT, PRIMARY KEY(id), FOREIGN KEY(carrinho_id) REFERENCES carrinho(id), FOREIGN KEY(usuario_id) REFERENCES usuario(nif) );"
    # db_cmd(sql)
    return redirect(url_for('main'))





###############################################################################
########################################################################## main
###############################################################################

@app.route("/main")
def main():
    return render_template('main.html')

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
###############################################################################

@app.route("/gerenciar/usuarios", methods=['GET','POST'])
def gerenciarusuarios(): # ucs, lista : usuarioNIF,nome,disciplina
    if request.method == 'POST':
        usuario.set_nif(request.form['usuarioNIF'])
        usuario.set_nome(request.form['usuarioNome'])
        usuario.set_disciplina(request.form['usuarioDisciplina'])
        return redirect(url_for('gerenciarusuariosadd'))
    else:
        sql = "SELECT * FROM disciplina;"
        ucs = db_cmd(sql)
        sql = "SELECT * FROM usuario;"
        lista = db_cmd(sql)
        return render_template('gerenciar_usuarios.html', lista=lista, ucs=ucs )

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




# @app.route("/tb_usuarios", methods=['GET', 'POST'])
# def tb_usuarios():
#     sql = "SELECT * FROM disciplina;"
#     ucs = db_cmd(sql)
#     if request.method == 'POST':
#         nif = request.form['usuarioNIF']
#         nome = request.form['usuarioNome']
#         disciplina = request.form['usuarioDisciplina']
#         sql =  "INSERT INTO usuario (nif, nome, disciplina) VALUES ('{}','{}','{}');".format(str(nif), str(nome), str(disciplina) )
#         db_cmd(sql)
#         return redirect(url_for('tb_usuarios'))
#     sql = "SELECT * FROM usuario;"
#     lista = db_cmd(sql)
#     return render_template('tb_usuarios.html', lista=lista, ucs=ucs)

# @app.route("/delusuario/<nif>", methods=['GET', 'POST'])
# def delusuario(nif):
#     sql = "DELETE FROM usuario WHERE nif='{}';".format(nif)
#     db_cmd(sql)
#     return redirect(url_for('tb_usuarios'))







@app.route("/gerenciar/carrinhos")
def gerenciarcarrinhos():
    return render_template('gerenciar_carrinhos.html')

@app.route("/gerenciar/equipamentos")
def gerenciarequipamentos():
    return render_template('gerenciar_equipamentos.html')

@app.route("/gerenciar/reservas")
def gerenciarreservas():
    return render_template('gerenciar_reservas.html')




###############################################################################
###############################################################################
###############################################################################

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

###############################################################################
###############################################################################
###############################################################################





# class Calendario:
#     def __init__(self):
#         self.data = ""
#     def set(self, dt ):
#         self.data = dt
#     def get(self):
#         return(self.data)

# class Carrinho:
#     def __init__(self):
#         self.carrinho = ""
#     def set(self, lista ):
#         self.carrinho = lista
#     def get(self):
#         return(self.carrinho)

# class Acesso:
#     def __init__(self):
#         self.uc = ''
#         self.user = ''
#         self.pwd = ''
#     def set_uc(self, uc):
#         self.uc = uc
#     def set_user(self, user):
#         self.user = user
#     def set_pwd(self,pwd):
#         self.pwd = pwd
#     def get_uc(self):
#         return(self.uc)
#     def get_user(self):
#         return(self.user)
#     def get_pwd(self):
#         return(self.pwd)

# class LoginAcesso:
#     def __init__(self):
#         self.msg = ""
#         self.campo = ""
#         self.sql = ""
#     def set(self, m,c,s):
#         self.msg = m
#         self.campo = c
#         self.sql = s
#     def get_msg(self):
#         return(self.msg)
#     def get_campo(self):
#         return(self.campo)
#     def get_sql(self):
#         return(self.sql)










# car = Carrinho()
# cal = Calendario()
# acesso = Acesso()
# loginAcesso = LoginAcesso()




# @app.route("/", methods=['GET','POST'])
# def index():
#     if request.method == 'POST':
#         botao = request.form['botao']
#         if botao == 'Agendar':
#             return redirect(url_for('create_tables'))
#         else:
#             return redirect(url_for('config'))
#     return render_template('index.html')


# @app.route("/createtables")
# def create_tables():
#     sql = "CREATE TABLE IF NOT EXISTS pi1_db.disciplina( codigo varchar(6) not null, nome varchar(50) not null, primary key(codigo));"
#     db_cmd(sql)
#     sql = "CREATE TABLE IF NOT EXISTS pi1_db.usuario( nif INT NOT NULL, nome VARCHAR(50) NOT NULL, disciplina VARCHAR(6), PRIMARY KEY(nif), FOREIGN KEY(disciplina) REFERENCES disciplina(codigo) );"
#     db_cmd(sql)
#     sql = "CREATE TABLE IF NOT EXISTS pi1_db.carrinho( id INT NOT NULL, nome VARCHAR(16) NOT NULL, qtd_equipamentos INT, PRIMARY KEY(id));"
#     db_cmd(sql)
#     sql = "CREATE TABLE IF NOT EXISTS pi1_db.equipamento( np INT NOT NULL, nome VARCHAR(20) NOT NULL, carrinho INT, descricao VARCHAR(50), adquirido_em DATE, status VARCHAR(16), PRIMARY KEY(np));"
#     db_cmd(sql)
#     sql = "CREATE TABLE IF NOT EXISTS pi1_db.reserva( id INT NOT NULL AUTO_INCREMENT, data DATE, carrinho_id INT, usuario_id INT, PRIMARY KEY(id), FOREIGN KEY(carrinho_id) REFERENCES carrinho(id), FOREIGN KEY(usuario_id) REFERENCES usuario(nif) );"
#     db_cmd(sql)
#     return redirect(url_for('prelogin'))


# @app.route("/prelogin")
# def prelogin():
#     loginAcesso.set("Escolha a unidade curricular:","disciplina","SELECT codigo,nome FROM disciplina;")
#     return redirect(url_for('login'))


# @app.route("/login")
# def login():
#     lista = db_cmd(loginAcesso.get_sql())
#     return render_template('login.html', msg=loginAcesso.get_msg(), campo=loginAcesso.get_campo(), lista=lista )

# @app.route("/login/disciplina/<uc>")
# def login_disciplina(uc):
#     acesso.set_uc( uc )
#     loginAcesso.set("Escolha o usuário de acesso:","usuario","SELECT nif,nome FROM usuario WHERE disciplina='{}';".format(acesso.get_uc()))
#     return redirect(url_for('login'))

# @app.route("/login/usuario/<nif>")
# def login_usuario(nif):
#     acesso.set_user(nif)
#     return redirect(url_for('loginsenha'))

# @app.route("/loginsenha", methods=['GET','POST'])
# def loginsenha():
#     if request.method == 'POST':
#         acesso.set_pwd(request.form['pwd'])
#         return redirect(url_for('manager'))
#     return render_template('loginsenha.html');



# @app.route("/manager", methods=['GET', 'POST'])
# def manager():
#     sql = "SELECT * FROM reserva WHERE data=CURDATE();"
#     lista = db_cmd(sql)
#     # imp = ""
#     # cal.set(lista[1])
#     if request.method == 'POST':
#         cal.set(request.form['calendario'])
#         sql =  "SELECT * FROM reserva WHERE data='{}' ORDER BY carrinho_id;".format( cal.get() )
#         lista = db_cmd(sql)
#         sql = "SELECT id,nome FROM carrinho WHERE id NOT IN (SELECT carrinho_id FROM reserva where data='{}' ORDER BY carrinho_id);".format(cal.get())
#         car.set( db_cmd(sql) )
#     return render_template('manager.html', lista=lista, car=car.get(), cal=cal.get(), user=acesso.get_user())

# @app.route("/manager/<car_id>")
# def manager_car(car_id):
#     sql =  "INSERT INTO reserva (data, carrinho_id, usuario_id) VALUES ('{}', '{}', '{}');".format(cal.get(), car_id, acesso.get_user())
#     db_cmd(sql)
#     return redirect(url_for('manager'))
    

# @app.route("/manager/delreserva/<id>", methods=['GET', 'POST'])
# def managerdelreserva(id):
#     sql = "DELETE FROM reserva WHERE id='{}';".format(id)
#     db_cmd(sql)
#     return redirect(url_for('manager'))


# ###############################################################################
# ###      PI1_DB Configurações
# ###############################################################################
# @app.route("/config", methods=['GET', 'POST'])
# def config():
#     return render_template('config.html')



# ###############################################################################
# ###      PI1_DB Disciplinas
# ###############################################################################

# @app.route("/tb_disciplinas", methods=['GET', 'POST'])
# def tb_disciplinas():
#     editar = ['','']
#     if request.method == 'POST':
#         codigo = request.form['disciplinaCodigo']
#         nome = request.form['disciplinaNome']
#         sql =  "INSERT INTO disciplina (codigo, nome) VALUES ('{}', '{}');".format(str(codigo), str(nome))
#         db_cmd(sql)
#         return redirect(url_for('tb_disciplinas'))
#     sql = "SELECT * FROM disciplina;"
#     lista = db_cmd(sql)
#     return render_template('tb_disciplinas.html', lista=lista, editar=editar)

# @app.route("/deldisciplina/<codigo>", methods=['GET', 'POST'])
# def deldisciplina(codigo):
#     sql = "DELETE FROM disciplina WHERE codigo='{}';".format(codigo)
#     db_cmd(sql)
#     return redirect(url_for('tb_disciplinas'))



# ###############################################################################
# ###      PI1_DB Usuarios
# ###############################################################################

# @app.route("/tb_usuarios", methods=['GET', 'POST'])
# def tb_usuarios():
#     sql = "SELECT * FROM disciplina;"
#     ucs = db_cmd(sql)
#     if request.method == 'POST':
#         nif = request.form['usuarioNIF']
#         nome = request.form['usuarioNome']
#         disciplina = request.form['usuarioDisciplina']
#         sql =  "INSERT INTO usuario (nif, nome, disciplina) VALUES ('{}','{}','{}');".format(str(nif), str(nome), str(disciplina) )
#         db_cmd(sql)
#         return redirect(url_for('tb_usuarios'))
#     sql = "SELECT * FROM usuario;"
#     lista = db_cmd(sql)
#     return render_template('tb_usuarios.html', lista=lista, ucs=ucs)

# @app.route("/delusuario/<nif>", methods=['GET', 'POST'])
# def delusuario(nif):
#     sql = "DELETE FROM usuario WHERE nif='{}';".format(nif)
#     db_cmd(sql)
#     return redirect(url_for('tb_usuarios'))



# ###############################################################################
# ###      PI1_DB Carrinhos
# ###############################################################################

# @app.route("/tb_carrinhos", methods=['GET', 'POST'])
# def tb_carrinhos():
#     if request.method == 'POST':
#         id = request.form['carrinhoId']
#         nome = request.form['carrinhoNome']
#         sql =  "INSERT INTO carrinho (id, nome) VALUES ('{}','{}');".format(str(id), str(nome) )
#         db_cmd(sql)
#         return redirect(url_for('tb_carrinhos'))
#     sql = "SELECT * FROM carrinho;"
#     lista = db_cmd(sql)
#     return render_template('tb_carrinhos.html', lista=lista)

# @app.route("/delcarrinho/<id>", methods=['GET', 'POST'])
# def delcarrinho(id):
#     sql = "DELETE FROM carrinho WHERE id='{}';".format(id)
#     db_cmd(sql)
#     return redirect(url_for('tb_carrinhos'))


# ###############################################################################
# ###      PI1_DB Equipamentos
# ###############################################################################

# @app.route("/tb_equipamentos", methods=['GET', 'POST'])
# def tb_equipamentos():
#     if request.method == 'POST':
#         np = request.form['equipNumPatr']
#         nome = request.form['equipNome']
#         car = request.form['equipCarrinho']
#         descricao = request.form['equipDescricao']
#         aquisicao = request.form['equipAquisicao']
#         status = request.form['equipStatus']
#         sql =  "INSERT INTO equipamento (np, nome, carrinho, descricao, adquirido_em, status) VALUES ('{}','{}','{}','{}','{}','{}');".format(str(np), str(nome), str(car), str(descricao), str(aquisicao), str(status) )
#         db_cmd(sql)
#         return redirect(url_for('tb_equipamentos'))
#     sql = "SELECT * FROM equipamento;"
#     lista = db_cmd(sql)
#     sql = "SELECT id,nome FROM carrinho;"
#     carrinho = db_cmd(sql)
#     return render_template('tb_equipamentos.html', lista=lista, carrinho=carrinho)

# @app.route("/delequipamento/<np>", methods=['GET', 'POST'])
# def delequipamento(np):
#     sql = "DELETE FROM equipamento WHERE np='{}';".format(np)
#     db_cmd(sql)
#     return redirect(url_for('tb_equipamentos'))




# ###############################################################################
# ###      PI1_DB Reservas
# ###############################################################################

# @app.route("/tb_reservas", methods=['GET', 'POST'])
# def tb_reservas():
#     if request.method == 'POST':
#         cal_ = request.form['calendario']
#         car_ = request.form['carrinho']
#         usr_ = request.form['usuario']
#         sql =  "INSERT INTO reserva (data, carrinho_id, usuario_id) VALUES ('{}','{}','{}');".format(str(cal_), str(car_), str(usr_))
#         db_cmd(sql)
#         return redirect(url_for('tb_reservas'))
#     sql = "SELECT * FROM carrinho;"
#     car = db_cmd(sql)
#     sql = "SELECT * FROM usuario;"
#     usr = db_cmd(sql)
#     sql = "SELECT * FROM reserva;"
#     lista = db_cmd(sql)
#     return render_template('tb_reservas.html', lista=lista, car=car, usr=usr )

# @app.route("/delreserva/<id>", methods=['GET', 'POST'])
# def delreserva(id):
#     sql = "DELETE FROM reserva WHERE id='{}';".format(id)
#     db_cmd(sql)
#     return redirect(url_for('tb_reservas'))

# ###############################################################################
# ###      PI1_DB DROP ALL TABLES
# ###############################################################################
# @app.route("/dropalltables")
# def dropalltables():
#     sql = "DROP TABLE IF EXISTS reserva;"
#     db_cmd(sql)
#     sql = "DROP TABLE IF EXISTS equipamento;"
#     db_cmd(sql)
#     sql = "DROP TABLE IF EXISTS carrinho;"
#     db_cmd(sql)
#     sql = "DROP TABLE IF EXISTS usuario;"
#     db_cmd(sql)
#     sql = "DROP TABLE IF EXISTS disciplina;"
#     db_cmd(sql)
#     return redirect(url_for('login'))

###############################################################################
###############################################################################

