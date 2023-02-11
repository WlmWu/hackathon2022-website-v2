import argparse
from flask import Flask, request
from flask_restful import Resource, Api
import socket
from waitress import serve

from searchDB import DBSearcher

class Data(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.db = DBSearcher()

    def post(self):
        rcv = request.get_json()
        r, u = int(rcv.get('range')), rcv.get('unit')
        return self.db.searching(range=r, unit=u)

app = Flask(__name__)

@app.route("/")
def index():
    return "<h1>Hello World!</h1>"


api = Api(app)
api.add_resource(Data, '/data')
# app.run(port=8080)

if __name__ == '__main__':

    parser = argparse.ArgumentParser('Server script')
    parser.add_argument('-p', dest='port', type=int, default=8080)
    args = parser.parse_args()


    api = Api(app)
    api.add_resource(Data, '/data')

    ip = socket.gethostbyname(socket.gethostname())
    print(f'Flask Server Starts on {ip}:{args.port}...')
    serve(app, host=ip, port=args.port)
    app.run()