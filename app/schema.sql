DROP TABLE IF EXISTS reserva;
DROP TABLE IF EXISTS equipamento;
DROP TABLE IF EXISTS carrinho;
DROP TABLE IF EXISTS usuario;
DROP TABLE IF EXISTS disciplina;


CREATE TABLE IF NOT EXISTS pi1_db.disciplina( 
    codigo varchar(6) not null, 
    nome varchar(50) not null, 
    primary key(codigo)
    );
    
CREATE TABLE IF NOT EXISTS pi1_db.usuario( 
    nif INT NOT NULL, 
    nome VARCHAR(50) NOT NULL, 
    disciplina VARCHAR(6), 
    senha VARCHAR(50), 
    PRIMARY KEY(nif), 
    FOREIGN KEY(disciplina) REFERENCES disciplina(codigo) 
    );

CREATE TABLE IF NOT EXISTS pi1_db.carrinho( 
    id INT NOT NULL, 
    nome VARCHAR(16) NOT NULL, 
    qtd_equipamentos INT, PRIMARY KEY(id)
    );

CREATE TABLE IF NOT EXISTS pi1_db.equipamento( 
    np INT NOT NULL, 
    nome VARCHAR(20) NOT NULL, 
    carrinho INT, 
    descricao VARCHAR(50), 
    adquirido_em DATE, 
    status VARCHAR(16), 
    PRIMARY KEY(np)
    );

CREATE TABLE IF NOT EXISTS pi1_db.reserva( 
    id INT NOT NULL AUTO_INCREMENT, 
    data DATE, 
    carrinho_id INT, 
    usuario_id INT, 
    PRIMARY KEY(id), 
    FOREIGN KEY(carrinho_id) REFERENCES carrinho(id), 
    FOREIGN KEY(usuario_id) REFERENCES usuario(nif) 
    );
