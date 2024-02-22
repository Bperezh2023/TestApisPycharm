from flask import Flask
from api_rest.Views.r_view import rest_blueprint

app = Flask('APIREST_SGS')

app.register_blueprint(rest_blueprint)

if __name__ == '__main__':
    ##192.168.176.86 / 172.17.194.115
    app.run(host='172.17.195.180', port=5000, debug=True)
