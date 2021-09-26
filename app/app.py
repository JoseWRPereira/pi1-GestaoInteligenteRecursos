from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

@app.route("/")
def index():
    str = request.args.get('fname')
    curso = request.args.get('course')
    if( str == "Jose"):
        return "TesteVars: "+str+curso
    else:
        return render_template('index.html')


@app.route("/consulta")
def pages():
    return render_template('/pages/consulta.html')



app.run(host="0.0.0.0", port=5000)
