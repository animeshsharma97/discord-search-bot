from flask import Flask
from threading import Thread
from os import getenv

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello. I am gonna run indefinitely!"

def run():
  app.run(host="0.0.0.0", port=getenv("PORT", 8080), debug=False)

def keep_alive():
    t = Thread(target=run)
    t.start()
