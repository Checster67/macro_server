import os
import datetime
from datetime import datetime

# base directory for data
DATA_DIR = os.path.join(os.getcwd(), "_data")
ENTRIES_DIR = os.path.join(DATA_DIR, "entries")
INGREDIENTS_FILE = os.path.join(DATA_DIR, "ingredients.txt")
WEIGHTS_FILE = os.path.join(DATA_DIR, "weights.txt")


def checkDir(path):
    if not os.path.exists(path): 
        os.makedirs(path)


def checkFile(path):
    if not os.path.exists(path): 
        with open(path,'w') as file:
            file.write("")


def addIngredient(label, carb, prot, fat, kcals):
    """Amounts should be specified per 100 g of the ingredient"""
    with open(INGREDIENTS_FILE, "a") as file:
        label = label.replace(" ", "_")
        file.write(f"{label.upper()}-{carb}-{prot}-{fat}-{kcals}\n")


def getDate():
    current_date = datetime.now()
    formatted_date = current_date.strftime("%d-%m-%Y")
    return formatted_date


def getKals(c,p,f):
    return c*4+p*4+f*9

def getIngredients():
    with open(INGREDIENTS_FILE,"r") as file:
        text = file.read()
    text = text.split("\n")

    dict_ = {}

    for ing in text:
        s = ing.split("-")
        if len(s) > 1:
            dict_[s[0].strip()] = {
                    "carb":float(s[1]),
                    "prot":float(s[2]),
                    "fat":float(s[3]),
                    "kcals":float(s[4])
                    }

    return dict_


def logWeight(token):
    date = getDate()
    token = float(token)

    with open(WEIGHTS_FILE,"a") as file:
        file.write(f"{date}\t/\t{token} kg\n")


def processDayToken(token,file):
    '''
    example token: cottage cheese-200,bread marron-40,tuna-155,honey-10
    '''
    token = token.split(",")

    # get dictionary
    dict_ = getIngredients()

    entry = {"carb":0,"prot":0,"fat":0,"kcals":0}

    summary = "LABEL -- carb -- prot -- fat -- kcals\n\n"

    for tok in token:
        t = tok.split("-")

        label = t[0].strip().replace(" ","_").upper()

        if label == "MANUAL":
            macros = t[1].strip().split("_")
            carb = float(macros[0])
            prot = float(macros[1])
            fat = float(macros[2])
            kcals = float(macros[3])
        else:
            # we divide by 100 here since we specify every per 100g
            # mass here is therefore a factor, not an absolute mass 
            mass = float(t[1])/100
            
            carb = mass*dict_[label]["carb"]
            prot = mass*dict_[label]["prot"]
            fat = mass*dict_[label]["fat"]
            kcals = mass*dict_[label]["kcals"]

        summary = summary + f"{t[0]} -- {carb} -- {prot} -- {fat} -- {kcals}\n"

        entry["carb"]+=carb
        entry["prot"]+=prot
        entry["fat"]+=fat
        entry["kcals"]+=kcals

    summary = summary + "\n\n"
    summary = summary + f"TOTAL ---> {entry['carb']} -- {entry['prot']} -- {entry['fat']} -- {entry['kcals']}\n"

    with open(file,"w") as file:
        file.write(summary)

    return summary



def getWeightInsight(data: str, start_date: str = None):
    '''
    @GPT-5
    Calculates average weight change per day and per week.
    Optionally starts from a specified date (DD-MM-YYYY).
    '''
    # split lines and filter out empty ones
    lines = [line.strip() for line in data.strip().splitlines() if line.strip()]
    
    # parse date and weight into tuples
    records = []
    for line in lines:
        date_str, weight_str = line.split('/')
        date = datetime.strptime(date_str.strip(), "%d-%m-%Y")
        weight = float(weight_str.replace("kg", "").strip())
        records.append((date, weight))
    
    # sort by date (in case it's not ordered)
    records.sort(key=lambda x: x[0])
    
    # apply start date filter if provided
    if start_date:
        start_dt = datetime.strptime(start_date, "%d-%m-%Y")
        records = [r for r in records if r[0] >= start_dt]
    
    if len(records) < 2:
        raise ValueError("Not enough valid data points after applying start date.")
    
    # calculate total weight gain and total days
    total_days = (records[-1][0] - records[0][0]).days
    total_gain = records[-1][1] - records[0][1]
    
    # average per day and per week
    avg_per_day = total_gain / total_days if total_days > 0 else 0
    avg_per_week = avg_per_day * 7

    # print summary
    '''
    print(f"Data range: {records[0][0].strftime('%d-%m-%Y')} to {records[-1][0].strftime('%d-%m-%Y')}")
    print(f"Total change: {total_gain:.2f} kg over {total_days} days")
    print(f"Average weight change per day: {avg_per_day:.3f} kg/day")
    print(f"Average weight change per week: {avg_per_week:.3f} kg/week")
    '''

    return {
        "total_days": total_days,
        "total_change": total_gain,
        "avg_per_day": avg_per_day,
        "avg_per_week": avg_per_week
    }





