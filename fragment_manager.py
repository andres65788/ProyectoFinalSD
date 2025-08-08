from flask import Flask, jsonify
import os

app = Flask(__name__)

FRAGMENTS_FOLDER = "fragments"

@app.route('/fragments', methods=['GET'])
def list_fragments():
    fragments = sorted([f for f in os.listdir(FRAGMENTS_FOLDER) if f.endswith('.bin')])
    return jsonify(fragments)

if __name__ == '__main__':
    app.run(port=5001)
