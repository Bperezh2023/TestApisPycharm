from flask import Flask
from Views.r_view import rest_blueprint
from conf import host

app = Flask(__name__)

app.register_blueprint(rest_blueprint)

if __name__ == '__main__':
    ##192.168.176.86 / 172.17.194.115
    app.run(host, port=5000, debug=True)
