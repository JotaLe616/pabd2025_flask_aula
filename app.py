from flask import Flask, render_template, redirect, request, url_for
from datetime import datetime
from config.database import SupabaseConnection
from dao.funcionario_dao import FuncionarioDAO
from models.funcionario import Funcionario

app = Flask(__name__)

# Conexão com o DAO
client = SupabaseConnection().client
# DAO para acessar a tabela funcionário
funcionario_dao = FuncionarioDAO(client)

# Rota principal - lista com todos os funcionários
@app.route("/")
def index():
    return render_template("index.html", title="LOS POLLOS HERMANOS", app_name="LOS FUNCIONÁRIOS", funcionarios=funcionario_dao.read_all())

# Para formatar CPF
@app.template_filter('format_cpf')
def format_cpf(cpf):
    if not cpf or len(cpf) != 11:
        return cpf
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:11]}"

### READ - Para ver detalhes de um funcionário
@app.route("/funcionario/<string:pk>/<int:id>")
def read(pk, id):
    funcionario = funcionario_dao.read(pk, id)
    return render_template("read.html", funcionario=funcionario, datetime=datetime)

### CREATE - Para criar novo funcionário
@app.route('/funcionario/cadastrar', methods=['GET', 'POST'])
def create():
    # Se for POST, processa os dados do formulário
    if request.method == 'POST':
        # Coleta dos dados inseridos no formulário
        dados = request.form
            
        # Para converter os tipos de dados necessários
        from datetime import datetime as dt
        
        # Para converter a data de nascimento (string para date)
        if dados.get('data_nasc'):
            data_nasc = dt.strptime(dados['data_nasc'], '%Y-%m-%d').date()
        else:
            data_nasc = None
        
        # Para converter o salário (string para float)
        salario = float(dados.get('salario', 0.0))
        
        # Para converter o número de departamento (string para int)
        if dados.get('numero_departamento'):
            numero_departamento = int(dados['numero_departamento'])
        else:
            numero_departamento = None
        
        # Para validar o CPF do supervisor
        cpf_supervisor = dados.get('cpf_supervisor')
        if cpf_supervisor and cpf_supervisor.strip():
            cpf_supervisor = cpf_supervisor.replace('.', '').replace('-', '')
            if len(cpf_supervisor) != 11:
                cpf_supervisor = None
        else:
            cpf_supervisor = None
        
        # Para validar o CPF do funcionário
        try:
            cpf_funcionario = dados.get('cpf')
            if not cpf_funcionario or not cpf_funcionario.strip():
                raise ValueError("CPF do funcionário não informado")

            cpf_funcionario = cpf_funcionario.replace('.', '').replace('-', '').strip()

            # Se o CPF tiver caracteres não numéricos ou não tiver 11 dígitos, é inválido
            if len(cpf_funcionario) != 11 or not cpf_funcionario.isdigit():
                raise ValueError("CPF do funcionário inválido")

        except ValueError as e:
            return f"Erro: {str(e)}", 400

        # Para criar Funcionario
        novo_funcionario = Funcionario(
            _cpf=cpf_funcionario,
            _pnome=dados.get('pnome'),
            _unome=dados.get('unome'),
            _data_nasc=data_nasc,
            _endereco=dados.get('endereco'),
            _salario=salario,
            _sexo=dados.get('sexo'),
            _cpf_supervisor=cpf_supervisor,
            _numero_departamento=numero_departamento
        )
        
        # Para salvar no banco de dados
        funcionario_dao.create(novo_funcionario)
        return redirect(url_for('index'))
                
    # Se for GET, apenas mostra o formulário em branco
    else:        
        return render_template('create.html')

### EDIT - Para editar funcionário
# GET exibe formulário com dados atuais, POST processa atualização
@app.route('/funcionario/edit/<string:pk>', methods=['GET', 'POST'])
def edit(pk):
    funcionario_atual = funcionario_dao.read('cpf', pk)
    if not funcionario_atual:
        return "Funcionário não encontrado", 404

    if request.method == 'POST':     
        # Coleta dos dados inseridos no formulário
        dados = request.form
            
        # Para converter os tipos de dados necessários
        from datetime import datetime as dt
            
        # Se usuário atualizou a data
        if dados.get('data_nasc'):

            # Converte a data de nascimento (string para date)
            data_nasc = dt.strptime(dados['data_nasc'], '%Y-%m-%d').date()
        
        # Do contrário, mantém a data atual
        else:
            data_nasc = funcionario_atual.data_nasc
        
        # Pega salário do formulário, ou mantém o atual se não tiver sido atualizado
        salario = float(dados.get('salario', funcionario_atual.salario))
            
        # Se usuário atualizou o número do departamento    
        if dados.get('numero_departamento'):

            # Converte o número de departamento (string para int)
            numero_departamento = int(dados['numero_departamento'])

        # Do contrário, mantém o número do departamento atual    
        else:
            numero_departamento = funcionario_atual.numero_departamento
            
        # CPF supervisor
        cpf_supervisor = dados.get('cpf_supervisor')
        if cpf_supervisor and cpf_supervisor.strip():
            cpf_supervisor = cpf_supervisor.replace('.', '').replace('-', '')
            if len(cpf_supervisor) != 11:
                cpf_supervisor = None
        else:
            cpf_supervisor = None
        
        # Para atualizar Funcionário
        funcionario_atualizado = Funcionario(
            _cpf=pk,
            _pnome=dados.get('pnome', funcionario_atual.pnome),
            _unome=dados.get('unome', funcionario_atual.unome),
            _data_nasc=data_nasc,
            _endereco=dados.get('endereco', funcionario_atual.endereco),
            _salario=salario,
            _sexo=dados.get('sexo', funcionario_atual.sexo),
            _cpf_supervisor=cpf_supervisor,
            _numero_departamento=numero_departamento,
            _created_at=funcionario_atual.created_at
        )

        # Para salvar no banco de dados
        funcionario_dao.update('cpf', pk, funcionario_atualizado)
        return redirect(url_for('index'))

    # Se for GET, apenas mostra o formulário em branco
    else:        
        return render_template('edit.html', funcionario=funcionario_atual, datetime=datetime)

### DELETE - Para excluir funcionário
@app.route('/funcionario/delete/<string:pk>', methods=['GET', 'POST'])
def delete(pk):
    
    funcionario = funcionario_dao.read('cpf', pk)

    # Verifica se o funcionário existe antes de tentar excluir
    if not funcionario:
        return "Funcionário não encontrado", 404

    if request.method == 'POST':
        funcionario_dao.delete('cpf', pk)
        return redirect(url_for('index'))
        
    return render_template('delete.html', funcionario=funcionario, datetime=datetime)