import sys

import sqlConnector
import schedule

positionList = ['QB', 'RB', 'WR', 'TE', 'K', 'DEF']

def getPointsAgainst():

    tableName = 'ptsAgainst'
    titles = { 'team':'VARCHAR(255)', 'avgPtsAg':'FLOAT', 'position':'VARCHAR(255)' }
    #FIXME
    # If we have the table from before, drop it and regenerate?
    if ( db.checkTableExists( tableName ) == True ):
        db.dropTable( tableName )

    db.createTable( tableName, titles )

    #FIXME WE probably want to be able to discount the team we are interested from the ptsAgainst data due to skewing
    for team in schedule.schedule['2019']:
        if team != '':
            for pos in positionList:
                sqlString = "SELECT avg(ptsAg), opponent, position FROM ( SELECT week, ROUND( sum(weekPts), 1) AS ptsAg, opponent, position FROM weekStats WHERE position='" + pos + "' AND opponent='" + team + "' GROUP BY week ) as T";
                result = db.executeSelect( sqlString )
                lineDictList = []
                for line in result:
                    lineDict = {'team':team, 'position':pos, 'avgPtsAg':round( line[0], 2 ) }
                    db.insert( tableName, lineDict )
                        

def getPointsMult( playerInfo, predWeek ):
    ptsMultAvg = 0.0
    playerPct = 0.0
    plWeeksPlayed = 0
    teamWeeksPlayed = 0
    team = playerInfo['team']
    position = playerInfo['position']
    name = playerInfo['name']
    for i in range( 1, predWeek ):
        opponent = schedule.schedule['2019'][team][i]
        if ( opponent != 'BYE' ):
            teamWeeksPlayed += 1
            ptsAgString = "SELECT avgPtsAg, team FROM ptsAgainst WHERE team='" + opponent + "' AND position='" + position + "'";
            result = db.executeSelect( ptsAgString )
            oppAvgAg = result[0][0] 

            ptsForString = "SELECT ROUND( SUM( weekPts ), 2), teamAbbr, opponent FROM weekStats WHERE teamAbbr='" + team + "' and position='" + position + "' and week=" + str( i );
            result = db.executeSelect( ptsForString )
            teamPts = result[0][0]
            ptsMultAvg += teamPts/oppAvgAg

            playerString = "SELECT weekPts, name, opponent FROM weekStats WHERE name='" + name + "' and week=" + str( i );
            result = db.executeSelect( playerString )
            if ( result ):
                plWeeksPlayed += 1
                playerPts = result[0][0]
                playerPct += playerPts/teamPts
                #print( oppAvgAg, ptsFor, ptsFor/oppAvgAg )

    ptsMultAvg = ptsMultAvg / teamWeeksPlayed
    playerPct = playerPct / plWeeksPlayed

    print( round( ptsMultAvg, 2 ) )
    return ptsMultAvg, playerPct


def getPlayerInfo( player ):
    tableName = 'weekStats'
    sqlString = "SELECT name, teamAbbr, position FROM " + tableName + " WHERE name='" + player + "'"
    result = db.executeSelect( sqlString )
    playerInfo = {'name':player, 'team':result[0][1], 'position':result[0][2] }
    return playerInfo


if __name__=='__main__':
    maxWeek = 7 
    if len( sys.argv ) > 3:
        print( "Usage: getProjections.py playerName weekNumberToPredict" )
    elif len( sys.argv ) == 3:
        player = sys.argv[1]
        predWeek = int( sys.argv[2] )
    else:
        player = 'Noah Fant'
        predWeek = 7

    db = sqlConnector.sqlConnector()

    playerInfo = getPlayerInfo( player )

    #Build the points against table
    getPointsAgainst()

    pointsMult, playerPct = getPointsMult( playerInfo, predWeek )
    
    opponent = schedule.schedule['2019'][playerInfo['team']][predWeek]
    ptsAgString = "SELECT avgPtsAg, team FROM ptsAgainst WHERE team='" + opponent + "' AND position='" + playerInfo['position'] + "'";
    result = db.executeSelect( ptsAgString )
    oppAvgAg = result[0][0] 

    predTeamTotal = pointsMult * oppAvgAg
    print( "team prediction:", predTeamTotal )
    predPlayer = predTeamTotal * playerPct
    print( player, "predction", predPlayer )


