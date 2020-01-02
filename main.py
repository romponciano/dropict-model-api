import os
from hashlib import sha256
# externals must be added to requirements.txt
from flask import Flask, jsonify, request

app = Flask(__name__)

passAuth = '7a61b53701befdae0eeeffaecc73f14e20b537bb0f8b91ad7c2936dc63562b25'

def check_permissions():
  hashedWord = sha256(request.headers.get('Authorization').encode('utf-8')).hexdigest()
  print(hashedWord)
  if hashedWord == passAuth:
      return jsonify({"message": "a resposta para a vida, o universo e tudo mais"})
  return jsonify({"message": "Não entre em pânico!"})

@app.route('/')
def home():
  return check_permissions()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)