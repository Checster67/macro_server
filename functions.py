import os

def checkDir(path):
    if not os.path.exists(path): 
        os.makedirs(path)


def checkFile(path):
    if not os.path.exists(path): 
        with open(path,'w') as file:
            file.write("")


def addIngredient(label,carb,prot,fat):
    '''
    amounts should be specified per 100 of the ingredient
    '''
    with open("_data\\ingredients.txt","a") as file:
        label = label.replace(" ","_")
        file.write(f"{label.upper()}-{carb}-{prot}-{fat}\n")


def getKals(c,p,f):
    return c*4+p*4+f*9



