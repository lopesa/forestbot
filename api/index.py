from flask import Flask, request

app = Flask(__name__)

# @app.route("/api/python")
# def hello_world():
#     return "<p>Hello, World!</p>"

@app.route("/api/chat", methods=['POST'])
def main():
    # breakpoint()

    print('request.json', request.json)
    return 'cats' 