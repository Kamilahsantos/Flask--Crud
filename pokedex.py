from flask import Flask, render_template, request, redirect, session, flash, url_for
#render template: passando o nome do modelo e a variáveis ele vai renderizar o template
#request: faz as requisições da nosa aplicação
#redirect: redireciona pra outras páginas
#session: armazena informações do usuário
#flash:mensagem de alerta exibida na tela
#url_for: vai para aonde o redirect indica

app = Flask(__name__)
app.secret_key = 'flask'
#chave secreta da sessão

class Pokemon:
    def __init__(self, nome, especie, tipo):
        self.nome = nome
        self.especie = especie
        self.tipo = tipo

class Treinadora:
    def __init__(self, id, nome, senha):
        self.id = id
        self.nome = nome
        self.senha = senha

#criação das terindoras
treinadora1 = Treinadora('Mary', 'Mary Jackson ', '1234')
treinadora2 = Treinadora('Ada', 'Ada Lovelace', '1234')
treinadora3 = Treinadora('Katherine', 'Katherine Johnson', '1234')

treinadoras = {treinadora1.id: treinadora1,
            treinadora2.id: treinadora2,
            treinadora3.id: treinadora3}

#base de dados de pokemons
pokemon1 = Pokemon('Meowth', 'Arranha Gato', 'Normal')
pokemon2 = Pokemon('Charmander', 'Lagarto', 'Fogo')
pokemon3 = Pokemon('Clefairy', 'Fada', 'Fada')
pokemon4 = Pokemon('Machop', 'Superpoder', 'Lutador')
pokemon5 = Pokemon('Rhyhorn', 'Espigão', 'Terrestre/pedra')
pokemon6 = Pokemon('Cyndaquil', 'Rato de fogo', 'Fogo')
pokemon7 = Pokemon('Shuckle', 'Mofo', 'Pedra')
pokemon8 = Pokemon('Whismur', 'Sussuro', 'Normal')
pokemon9 = Pokemon('Swablu', 'Pássaro de algodão', 'Voador')
pokemon10 = Pokemon('Bidoof', 'Rato Gorducho', 'Normal')

lista = [pokemon1, pokemon2,pokemon3,pokemon4,pokemon5,pokemon6,pokemon7,pokemon8,pokemon9,pokemon10]

#configuração da rota index.
@app.route('/')
def index():
    return render_template('lista.html', titulo='Pokedex', pokemons=lista)
    #renderizando o template lista e as variáveis desejadas. 

#configuração da rota novo, ela só poderá ser acessda se o usuário estiver logado, caso contrário redireciona para a tela de login
@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
        return render_template('novo.html', titulo='Novo Pokemon')
        #renderiza o template novo

#configuração da rpta criar que usa o método post para enviar dados dos nossos pokemons
@app.route('/criar', methods=['POST',])
def criar():
    nome = request. form['nome']
    especie = request. form['especie']
    tipo = request. form['tipo']
    pokemon = Pokemon(nome, especie, tipo)
    lista.append(pokemon)
    return redirect(url_for('index'))
#já inclui o novo pokemon na lista e joga na tela inicial

#configuração da rota login
@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

#configuração da rota autenticar que verific as credenciais das terinadoras
@app.route('/autenticar', methods=['POST', ])
def autenticar():
    if request.form['treinadora'] in treinadoras:
        treinadora = treinadoras[request.form['treinadora']]
        if treinadora.senha == request.form['senha']:
            session['usuario_logado'] = treinadora.id
            flash(treinadora.nome + ' acesso permitido!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        #caso as credenciais não sejam validadas, exibe mensagem de erro e redirecion para o login
        flash('Acesso negado, digite novamente!')
        return redirect(url_for('login'))

#configuração da rota logout
@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Treinadora, logue novamente para cadastrar os pokemons que encontrar!')
    return redirect(url_for('index'))


app.run(debug=True)
