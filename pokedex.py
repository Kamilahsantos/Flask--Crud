from flask import Flask, render_template, request, redirect, session, flash, url_for

app = Flask(__name__)
app.secret_key = 'flask'

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


treinadora1 = Treinadora('Mary', 'Mary Jackson ', '1234')
treinadora2 = Treinadora('Ada', 'Ada Lovelace', '1234')
treinadora3 = Treinadora('Katherine', 'Katherine Johnson', '1234')

treinadoras = {treinadora1.id: treinadora1,
            treinadora2.id: treinadora2,
            treinadora3.id: treinadora3}


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

@app.route('/')
def index():
    return render_template('lista.html', titulo='Pokedex', pokemons=lista)

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Novo Pokemon')

@app.route('/criar', methods=['POST',])
def criar():
    nome = request. form['nome']
    especie = request. form['especie']
    tipo = request. form['tipo']
    pokemon = Pokemon(nome, especie, tipo)
    lista.append(pokemon)
    return redirect(url_for('index'))


@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)


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
        flash('Acesso negado, digite novamente!')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Treinadora, logue novamente para cadastrar os pokemons que encontrar!')
    return redirect(url_for('index'))


app.run(debug=True)
