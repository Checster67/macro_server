from flask import Flask, jsonify, request
from functions import *

# Initialize Flask app
app = Flask(__name__)


@app.route('/')
def home():
    return "Antoine's Central Server"





# MACRO CALCULATOR 
# -------------------------------------------------
checkDir("_data")
checkDir("_data\\entries")
checkFile("_data\\ingredients.txt")
checkFile("_data\\weights.txt")

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


@app.route('/macro/log-weight')
def log_weight():
    token = request.args["token"]
    logWeight(token)

    with open("_data\\weights.txt","r") as file:
        text = file.read()

    text = text.replace("\n","<br>")

    return text 



@app.route('/macro/weight-info')
def weight_info():
    try:
        token = request.args["token"]
    except:
        token = None
    
    with open("_data\\weights.txt","r") as file:
        text = file.read()

    answer = getWeightInsight(text,token)

    answer = f'''
    TOTAL DAYS-------{round(answer["total_days"],4)} days<br>
    TOTAL CHANGE-----{round(answer["total_change"],4)} kg<br>
    AVG PER DAY------{round(answer["avg_per_day"],4)} kg/day<br>
    AVG PER WEEK-----{round(answer["avg_per_week"],4)} kg/week<br>
    '''
    
    return answer



@app.route('/macro/process-day-token')
def process_day_token():
    today = getDate()
    checkFile(f"_data\\entries\\{today}.txt")

    token = request.args["token"]

    summary = processDayToken(token,
                              f"_data\\entries\\{today}.txt")

    summary = summary.replace("\n","<br>")
    
    return summary





if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)




