from flask import Flask, request
import datetime
import sys
import hashlib

app = Flask(__name__)

@app.route("/")
def hello_world():
	return "Hello, world!"