# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
import os

from spo import get_info
from net import get_song_name, get_artisit_name


app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

# endpoint to show all users
@app.route("/song/<id>", methods=["GET"])
def get_json(id):
    name = get_song_name(id)
    artist = get_artisit_name(id)
    info = get_info(name, artist, id)
    return jsonify(info)




if __name__ == '__main__':
    app.run(debug=True)


#print(info)