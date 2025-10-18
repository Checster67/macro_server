from flask import Flask, jsonify, request
from functions import *

# Initialize Flask app
app = Flask(__name__)

checkDir("_data")
checkDir("_data\\entries")
checkFile("_data\\ingredients.txt")

@app.route('/')
def home():
    return "Antoine's Central Server"





# MACRO CALCULATOR 
# -------------------------------------------------
@app.route('/macro/add')
def add_ingredient():
    token = request.args["token"]
    token = token.split(",")
    addIngredient(label=token[0].strip(),
                  carb=token[1].strip(),
                  prot=token[2].strip(),
                  fat=token[3].strip(),
                  kcals=token[4].strip())
    return f"Added! {token}"


@app.route('/macro/process_day_token')
def process_day_token():
    today = getDate()
    checkFile(f"_data\\entries\\{today}.txt")

    token = request.args["token"]

    summary = processDayToken(token,
                              f"_data\\entries\\{today}.txt")

    return summary





if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)




