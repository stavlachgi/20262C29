from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/public-data', methods=['GET'])
def get_public_data():
    data = {
        "status": "success",
        "message": "This is a public endpoint",
        "content": "No authentication required"
    }
    return jsonify(data), 200

if __name__ == '__main__':
    app.run(debug=True)
