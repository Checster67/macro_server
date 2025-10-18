import os
import datetime

def checkDir(path):
    if not os.path.exists(path): 
        os.makedirs(path)


def checkFile(path):
    if not os.path.exists(path): 
        with open(path,'w') as file:
            file.write("")


def addIngredient(label,carb,prot,fat,kcals):
    '''
    amounts should be specified per 100 of the ingredient
    '''
    with open("_data\\ingredients.txt","a") as file:
        label = label.replace(" ","_")
        file.write(f"{label.upper()}-{carb}-{prot}-{fat}-{kcals}\n")


def getDate():
    current_date = datetime.datetime.now()
    formatted_date = current_date.strftime("%d-%m-%Y")
    return formatted_date


def getKals(c,p,f):
    return c*4+p*4+f*9

def getIngredients():
    with open("_data\\ingredients.txt","r") as file:
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

    with open("_data\\weights.txt","a") as file:
        file.write(f"{date} ---------- {token} kg\n")


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

        label = t[0].replace(" ","_").upper()

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








