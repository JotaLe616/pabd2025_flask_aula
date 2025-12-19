from flask import Flask, render_template
from config.database import SupabaseConnection
from dao.funcionario_dao import FuncionarioDAO

app = Flask(__name__)

client = SupabaseConnection().client

# Criando DAO para acessar a tabela funcionario
funcionario_dao = FuncionarioDAO(client)

@app.route("/")
def hello_world():
    return render_template("index.html", title="3INF1M", app_name="Meu Flask App", funcionarios=funcionario_dao.read_all())
