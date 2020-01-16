import os
from hashlib import sha256
# externals must be added to requirements.txt
from flask import Flask, jsonify, request, make_response
from flask_cors import CORS, cross_origin
import joblib
import pandas as pd

dt_model = joblib.load('./static/dt.sav')
dnn_model = joblib.load('./static/dnn.sav')
knn_model = joblib.load('./static/knn.sav')

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

passAuth = '0e08e019a48d4f00860082806b81b1eedc275818d99246bd32576b799557fa20'

def check_permissions():
  hashedWord = sha256(request.headers.get('Authorization').encode('utf-8')).hexdigest()
  if hashedWord == passAuth:
      return -1
  return jsonify({"predict": "Sem permissão"})

def load_model(dataRow):
  selectedIa = str(request.headers.get('SelectedIA').encode('utf-8'))
  selected = (selectedIa.split("'"))[1]
  out = ''
  if(selected == 'knn'):
    out = knn_model.predict(dataRow)
    print('Predicao feita do knn: ', out)
  elif(selected == 'dt'):
    out = dt_model.predict(dataRow)
    print('Predicao feita do dt: ', out)
  elif(selected == 'dnn'):
    resp = dnn_model.predict(dataRow)
    print('Predicao feita do dnn: ', resp)
    out = resp[0][1]
  return out

@app.route('/predict', methods=['POST'])
@cross_origin()
def getPredict():
  out = check_permissions()
  if(out == -1): 
    data = [[
      request.json['forum'],
      request.json['mod_discussion'],
      request.json['total_acesso'],
      request.json['nota_ead'],
      request.json['nota_alg'],
      request.json['nota_fdw'],
      request.json['nota_fmi'],
      request.json['nota_mat'],
      request.json['sexo'],
      request.json['idade'],
      request.json['e_civil'],
      request.json['raca'],
      request.json['trabalha'],
      request.json['qtde_resid_casa'],
      request.json['renda_familiar'],
      request.json['pc_casa']
    ]]
    
    df = pd.DataFrame(data, columns =[
      'FORUM', 'MOD_DISCUSSION', 'TOTAL_ACESSO', 'NOTA_EAD', 'NOTA_ALG', 'NOTA_FDW',
      'NOTA_FMI', 'NOTA_MAT', 'Sexo', 'Idade', 'E_Civil', 'Raca', 'trabalha', 
      'qtde_resid_casa', 'Renda_Familiar', 'PC_casa'
    ])

    resposta = 'error'
    if(load_model(df) == 0):
      resposta = 'nao'
    else:
      resposta = 'sim'
    
    return make_response(jsonify({'predict': resposta}), 200)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == "__main__":
    dt_model = joblib.load('./static/dt.sav')
    dnn_model = joblib.load('./static/dnn.sav')
    knn_model = joblib.load('./static/knn.sav')

    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)