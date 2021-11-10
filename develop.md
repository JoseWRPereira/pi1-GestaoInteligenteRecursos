
# Instalação

* Framework de desenvolvimento web: Flask
```
pip3 install Flask
```


* Instalação do gerenciador de banco de dados
```
pip3 install mariadb
```


# Desenvolvimento

* Ativando o ambiente virtual
```
cd app
source bin/activate
```

* Exportando variáveis de ambiente
```
export FLASK_APP=app
export FLASK_ENV=development
```

* Executando aplicação
```
flask run
```

# Deploy

* Instalação do servidor web para o Flask: Gunicorn
```
pip3 install gunicorn
```

* Produzir lista de requisitos da aplicação
```
pip3 freeze > requirements.txt
```

* Criação de arquivo de execução do servidor pelo hospedeiro
```
vim Procfile
web: gunicorn app:app
```

* Criar conta no Heroku
[Heroku](https://id.heroku.com/login)

* Criar um novo app

* Instalar o [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) (Debian)
```
curl https://cli-assets.heroku.com/install-ubuntu.sh | sh
```

