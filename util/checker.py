number = True

def pwformat(t):
    num = False
    char = False
    for i in t:
        if "0" <= i and i <= "9":
            num = True
        if "a" <= i.lower() and i.upper() <= "z":
            char = True
    return num and char

def reformat(dic):
    for i in dic.keys():
        dic[i] = dic[i].replace("\r","")
    return dic
