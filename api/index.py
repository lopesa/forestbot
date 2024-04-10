from flask import Flask, request
from dotenv import load_dotenv
import os

load_dotenv()
test_env_variable = os.environ.get('TEST_ENV_VARIABLE')
# env = os.environ
# print('env', env)


app = Flask(__name__)

@app.route("/api/chat", methods=['POST'])
def main():
    return 'cats' 