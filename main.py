import os
from hashlib import sha256
import json
# externals must be added to requirements.txt
from flask import Flask, jsonify, request, make_response

app = Flask(__name__)

passAuth = '0e08e019a48d4f00860082806b81b1eedc275818d99246bd32576b799557fa20'

def check_permissions():
  hashedWord = sha256(request.headers.get('Authorization').encode('utf-8')).hexdigest()
  if hashedWord == passAuth:
      return -1
  return jsonify({"message": "Sem permissão"})

@app.route('/')
def home():
  out = check_permissions()
  if(out == -1):
    return jsonify({"message": "Com permissão"})
  else:
    return out

@app.route('/predict')
def getPredict():
  out = check_permissions()
  if(out == -1): 
    row = []
    row.append(request.json['forum'])
    row.append(request.json['mod_discussion'])
    row.append(request.json['total_acesso'])
    row.append(request.json['nota_ead'])
    row.append(request.json['nota_alg'])
    row.append(request.json['nota_fdw'])
    row.append(request.json['nota_fmi'])
    row.append(request.json['nota_mat'])
    row.append(request.json['sexo'])
    row.append(request.json['idade'])
    row.append(request.json['e_civil'])
    row.append(request.json['raca'])
    row.append(request.json['trabalha'])
    row.append(request.json['qtde_resid_casa'])
    row.append(request.json['renda_familiar'])
    row.append(request.json['pc_casa'])
    return make_response(jsonify({'predict': 'NAO'}), 200)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)