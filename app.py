from flask import Flask, request
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

@app.route('/save_data', methods=['POST'])
def save_data():
    data = request.get_json()
    with open('data.txt', 'a') as f:  # 'a' opens the file in append mode
        f.write(json.dumps(data) + '\n')  # '\n' adds a new line after each entry
    return 'Data saved'

if __name__ == '__main__':
    app.run(port=5000)
