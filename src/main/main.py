from flask import Flask, request, render_template
from flask_basicauth import BasicAuth
from sklearn.feature_extraction.text import CountVectorizer
from gensim.models import KeyedVectors
import string
import nltk
import numpy as np
nltk.download('punkt')
import os
import pickle


#read_modelo
with open('..\..\models\skip_model.pkl', 'rb') as f:
    modelo = pickle.load(f)
#colunas = ['tamanho','ano','garagem']
#caminho para appengine
#modelo = pickle.load(open('models/modelo.sav', 'rb'))
#caminho para Docker
#modelo = pickle.load(open('models/modelo.sav', 'rb'))

app = Flask(__name__, template_folder="../../templates", static_folder='../../static')
#app.config['BASIC_AUTH_USERNAME'] = os.environ.get('BASIC_AUTH_USERNAME')
#app.config['BASIC_AUTH_PASSWORD'] = os.environ.get('BASIC_AUTH_PASSWORD')
#basic_auth = BasicAuth(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/vies',methods=['POST'])
#@basic_auth.required
def pipe():
  frase = next(request.form.values())
  textos = frase.lower()
  lista_alfanumerico = []
  for token_valido in nltk.word_tokenize(textos):
      if token_valido in string.punctuation: continue
      lista_alfanumerico.append(token_valido)

  vetor_resultante = np.zeros(300)
  for pn in lista_alfanumerico:
      try:
          vetor_resultante += modelo.get_vector(pn)
      except KeyError:
          if pn.isnumeric():
              pn = "0"*len(pn)
              vetor_resultante += modelo.get_vector(pn)
          else:
              vetor_resultante += modelo.get_vector("unknown")
  resultado_1 = modelo.most_similar(vetor_resultante)[1][0]
  resultado_2 = modelo.most_similar(vetor_resultante)[2][0]
  resultado_3 = modelo.most_similar(vetor_resultante)[3][0]
  resultado_4 = modelo.most_similar(vetor_resultante)[4][0]
  resultado_5 = modelo.most_similar(vetor_resultante)[5][0]
  resultado_6 = modelo.most_similar(vetor_resultante)[6][0]
  resultado_7 = modelo.most_similar(vetor_resultante)[7][0]
  resultado_8 = modelo.most_similar(vetor_resultante)[8][0]

  return render_template('index.html',
                            title='Palavra: {}'.format(frase), 
                            category_1='Resultado 1: {}'.format(resultado_1),
                            category_2='Resultado 2: {}'.format(resultado_2),
                            category_3='Resultado 3: {}'.format(resultado_3),
                            category_4='Resultado 4: {}'.format(resultado_4),
                            category_5='Resultado 5: {}'.format(resultado_5),
                            category_6='Resultado 6: {}'.format(resultado_6),
                            category_7='Resultado 7: {}'.format(resultado_7),
                            category_8='Resultado 8: {}'.format(resultado_8)
                        )

#@app.route('/cotacao/', methods=['POST'])
#@basic_auth.required
#def cotacao():
#    dados = request.get_json()
#    dados_input = [dados[col] for col in colunas]
#    preco = modelo.predict([dados_input])
#    return jsonify(preco=preco[0])

app.run(debug=True, host='0.0.0.0')