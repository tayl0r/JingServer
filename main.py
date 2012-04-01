from flask import Flask
from JingServer import JingServer

app = Flask(__name__)
app.secret_key = 'A84zn#Hdh,.!@#*0= 3hj'
jing = JingServer(app)

@app.route('/api/', methods=['POST', 'GET'])
def api():
    header = """<?xml version="1.0" encoding="utf-16"?>
"""
    return header + jing.api()

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=80,
        debug=True
    )