from flask import Flask, render_template
from config.database import SupabaseConnection
from dao.funcionario_dao import FuncionarioDAO

app = Flask(__name__)

client = SupabaseConnection().client

# Criando DAO para acessar a tabela funcionario
funcionario_dao = FuncionarioDAO(client)

@app.route("/")
def index():
    return render_template("index.html", title="3INF1M", app_name="Empresa 3INF1M", funcionarios=funcionario_dao.read_all())

@app.route("/funcionario/<string:pk>/<int:id>")
def details(pk, id):
    funcionario = funcionario_dao.read(pk, id)
    return render_template("details.html", funcionario=funcionario)

