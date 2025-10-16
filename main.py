from flask import Flask, jsonify, request

# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def home():
    return "Antoine's Central Server"


'''
@app.route('/api/greet', methods=['GET'])
def greet():
    name = request.args.get('name', 'Guest')
    return jsonify({"message": f"Hello, {name}!"})

@app.route('/api/echo', methods=['POST'])
def echo():
    data = request.get_json()
    return jsonify({
        "you_sent": data,
        "status": "success"
    })
'''

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)



