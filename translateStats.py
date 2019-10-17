translateDict = {
    '1':'Games',
    '2':'PassAtt',
    '3':'PassComp',
    #'4':'unknown'
    '5':'PassYds',
    '6':'PassTD',
    '7':'PassInt',
    '8':'SacksReceived', #What to call?
    '13':'RushAtt',
    '14':'RushYds',
    '15':'RushTD',
    '20':'Rec',
    '21':'RecYds',
    '22':'RecTD',
    '30':'FumblesLost',
    '31':'Fumbles',
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
    '45':'Sacks',
    '46':'IntDef',
    '47':'FumRec',
    '48':'FFum',
    '49':'Safety',
    '50':'DefTD',
    '51':'BlockPunts',
    '52':'STYds',
    '53':'STTD',
    '54':'PtsAllowed',
    '62':'YdsAgainst',
    }


if __name__ == "__main__":
    preTranslate = { '49':7, '37':3 }
    postTranslate = {}
    for key,value in preTranslate.items():
        postTranslate[translateDict[key]] = value

    print( postTranslate )
