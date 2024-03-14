from flask import Flask, request
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)


@app.route('/save_data', methods=['POST'])
def save_data():
    """
    Endpoint to save JSON data from a POST request into a text file
    """
    data = request.get_json()
    with open('data.txt', 'a') as f:
        f.write(json.dumps(data) + '\n')
    return 'Data saved'


if __name__ == '__main__':
    # Run the Flask app on port 5000
    app.run(port=5000)
