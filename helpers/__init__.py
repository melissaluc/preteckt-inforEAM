def cleanDict(dictObj={}):
    new_dict = {x:y for x,y in dictObj.items() if y!=0}
    return new_dict


