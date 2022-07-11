from flask import Flask, jsonify
from flask_cors import CORS 


app = Flask(__name__)
CORS(app)
@app.route('/get',methods=['GET'])
def get_message():
    print("running")
    return jsonify({ 'message':"Helloooooooooooooooooooooooooo"})


if __name__ == "__main__":
    app.run(debug=True)