from flask import Flask, render_template
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
  def get(self):
    return {'hello': 'world by get'}

  def post(self):
    return {'hello': 'world by post'}

  def put(self):
    return {'hello': 'world by put'}

  def delete(self):
    return {'hello': 'world by delete'}

api.add_resource(HelloWorld, '/hello')

@app.route('/')
def hello():
  return render_template('index.html')

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
