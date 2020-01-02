from flask import Flask

app = Flask(__name__, static_folder='static')

@app.route('/')
def home():
  return 'hello world'

@app.route('/predict')
def predict():
  return 'predict route'

if (__name__ == '__main__'):
  app.run(debug=True)