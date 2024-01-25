from flask import Flask
from api_rest.Views.r_view import rest_blueprint

app = Flask(__name__)

app.register_blueprint(rest_blueprint)

if __name__ == '__main__':
    app.run(host='192.168.176.86', port=5000, debug=True)
