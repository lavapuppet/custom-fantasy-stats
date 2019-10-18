translateDict = {
    '1':'games',
    '2':'passAtt',
    '3':'passComp',
    #'4':'unknown'
    '5':'passYds',
    '6':'passTD',
    '7':'passInt',
    '8':'sacksReceived', #What to call?
    '13':'rushAtt',
    '14':'rushYds',
    '15':'rushTD',
    '20':'rec',
    '21':'recYds',
    '22':'recTD',
    '30':'fumblesLost',
    '31':'fumbles',
    '32':'2Pt',
    '33':'XPMade',
    '34':'XPMiss',
    '35':'FG0-19',
    '36':'FG20-29',
    '37':'FG30-39',
    '38':'FG40-49',
    '39':'FG50o',
    '40':'FM0-19',
    '41':'FM20-29',
    '42':'FM30-39',
    '43':'FM40-49',
    '44':'FM50o',
    '45':'sacks',
    '46':'intDef',
    '47':'fumRec',
    '48':'fFum',
    '49':'safety',
    '50':'defTD',
    '51':'blockPunts',
    '52':'sTYds',
    '53':'sTTD',
    '54':'ptsAllowed',
    '62':'ydsAgainst',
    }


if __name__ == "__main__":
    preTranslate = { '49':7, '37':3 }
    postTranslate = {}
    for key,value in preTranslate.items():
        postTranslate[translateDict[key]] = value

    print( postTranslate )
