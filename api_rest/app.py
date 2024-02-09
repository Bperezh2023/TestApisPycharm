from flask import Flask
from api_rest.Views.r_view import rest_blueprint

app = Flask(__name__)

app.register_blueprint(rest_blueprint)

if __name__ == '__main__':
    ##192.168.176.86
    app.run(host='172.17.195.95', port=5000, debug=True)
