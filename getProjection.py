import sys

import sqlConnector
import schedule

positionList = ['QB', 'RB', 'WR', 'TE', 'K', 'DEF']

# This creates a table of points against all teams by weeks
def buildPointsAgainst( db, rebuild = False ):

    tableName = 'ptsAgainst'
    titles = { 'team':'VARCHAR(255)','opp':'VARCHAR(255)', 'weekPtsAg':'FLOAT', 'position':'VARCHAR(255)' }
    # If we have the table from before, rebuild it if the user wants, otherwise we're done
    if ( db.checkTableExists( tableName ) == True and rebuild == False):
        return
    elif ( rebuild == True ):
        db.dropTable( tableName )

    db.createTable( tableName, titles )

    #We discount the team we are interested from the ptsAgainst data due to skewing
    for team in schedule.schedule['2019']:
        if team != '':
            for pos in positionList:
                sqlString = "SELECT ROUND( sum(weekPts), 1) AS ptsAg,teamAbbr, week, opponent, position FROM weekStats WHERE position='" + pos + "' AND opponent='" + team + "' GROUP BY week";
                result = db.executeSelect( sqlString )
                lineDictList = []
                for line in result:
                    lineDict = {'team':team,'opp':line[1], 'position':pos, 'weekPtsAg':round( line[0], 2 ) }
                    db.insert( tableName, lineDict )
                        

def getPointsMult( db, playerInfo, predWeek ):
    W1 = 0.6
    W = [ 1-W1, W1 ]
    jcount = 0 
    games = 3
    team = playerInfo['team']
    position = playerInfo['position']
    name = playerInfo['name']
    wPtsMult = 0.0
    wPlayerPct = 0.0
    for j in [0,1]:
        ptsMultAvg = 0.0 #number measuring the strength of offense
        playerPct = 0.0 # number measuring the percentage of team points a player gets
        plWeeksPlayed = 0
        teamWeeksPlayed = 0
        for i in range( 1 + j*(predWeek - games ) , predWeek - games  + (j * games)  ):
            opponent = schedule.schedule['2019'][team][i]
            # Once we have actually played someone, get that team's average points against excluding ourselves.
            if ( opponent != 'BYE' ):
                teamWeeksPlayed += 1
                ptsAgString = "SELECT AVG( weekPtsAg ), team FROM ptsAgainst WHERE team='" + opponent + "' AND position='" + position + "' AND opp!='" + team + "'";
                #print( ptsAgString );
                result = db.executeSelect( ptsAgString )
                oppAvgAg = result[0][0] 

                ptsForString = "SELECT ROUND( SUM( weekPts ), 2), teamAbbr, opponent FROM weekStats WHERE teamAbbr='" + team + "' and position='" + position + "' and week=" + str( i );
                result = db.executeSelect( ptsForString )
                #print( ptsForString, result )
                teamPts = result[0][0]
                if ( result[0][0] != None ):
                    #print( "team", teamPts, oppAvgAg )
                    ptsMultAvg += teamPts/oppAvgAg

                    playerString = "SELECT weekPts, name, opponent FROM weekStats WHERE name='" + name + "' and week=" + str( i ) + " and position='" + position + "'";
                    result = db.executeSelect( playerString )
                    if ( result ):
                        plWeeksPlayed += 1
                        playerPts = result[0][0]
                        #print( "player", playerPts )
                        if teamPts != 0:
                            playerPct += playerPts/teamPts

        if plWeeksPlayed == 0:
            W[jcount] = 0
            W[(jcount+1) % 2] = 1
            wPlayerPct = wPlayerPct/(1-W1) 
        else:
            playerPct = playerPct / plWeeksPlayed

        ptsMultAvg = ptsMultAvg / teamWeeksPlayed
        jcount += 1

        if(j==0):
            wPtsMult += ptsMultAvg * (1 - W1)
            wPlayerPct += playerPct * W[0] 
        else:
            wPtsMult+=ptsMultAvg * W1 
            wPlayerPct += playerPct * W[1] 

    #print( round( ptsMultAvg, 2 ) )
    return wPtsMult, wPlayerPct


def getPlayerInfo( db, player ):
    tableName = 'weekStats'
    sqlString = "SELECT name, teamAbbr, position FROM " + tableName + " WHERE name LIKE '" + player + "' AND position IN ( 'QB', 'WR', 'RB', 'TE', 'K', 'DEF')"
    result = db.executeSelect( sqlString )
    playerInfo = {'name':player, 'team':result[0][1], 'position':result[0][2] }
    return playerInfo

# If the player has "'" characters they will break the sql query. escape them
# We do this by replacin all cases of ' with ''
def escapePlayer( player ):
    return player.replace( "'", "''" )

def getProjection( player, predWeek, db = None, rebuild = False ):

    if ( not db ):
        db = sqlConnector.sqlConnector()

    # Select the first player that matches the player string
    '''player = escapePlayer( player )
    possString = "SELECT name, teamAbbr FROM weekStats where name LIKE '" + player + "'" 
    possibles = db.executeSelect( possString )
    player = possibles[0][0]
    #print(player)'''
    
    # If the player has "'" characters they will break the sql query. escape them
    # Note that the user want's their player output in the format they usually see it, so don't overwrite the player name
    playerInfo = getPlayerInfo( db, escapePlayer( player ) )

    #FIXME Build the points against table if it does not already exist
    buildPointsAgainst( db, rebuild )

    opponent = schedule.schedule['2019'][playerInfo['team']][predWeek]
    if opponent != 'BYE':
        pointsMult, playerPct = getPointsMult( db, playerInfo, predWeek )
        
        ptsAgString = "SELECT AVG( weekPtsAg ), team FROM ptsAgainst WHERE team='" + opponent + "' AND position='" + playerInfo['position'] + "'";
        result = db.executeSelect( ptsAgString )
        oppAvgAg = result[0][0] 

        predTeamTotal = pointsMult * oppAvgAg
        #print( "team prediction:", predTeamTotal )
        predPlayer = predTeamTotal * playerPct
        #print( player, "predction", predPlayer )
    else:
        #print( player, "on bye!!" )
        predPlayer = 0

    return predPlayer


if __name__=='__main__':
    if len( sys.argv ) > 4:
        print( "Usage: getProjections.py playerName weekNumberToPredict toRebuildOrNotToRebuild" )
        exit()
    elif len( sys.argv ) == 4:
        rebuild = bool( sys.argv[3] )
    else:
        rebuild = False

    if len( sys.argv ) >= 3:
        player = sys.argv[1]
        predWeek = int( sys.argv[2] )
    else:
        player = 'Noah Fant'
        predWeek = 7

    db = sqlConnector.sqlConnector()

    # Select the first player that matches the player string
    player = escapePlayer( player )
    possString = "SELECT name, teamAbbr FROM weekStats where name LIKE '" + player + "' AND position IN ( 'QB', 'WR', 'RB', 'TE', 'K', 'DEF')"
    possibles = db.executeSelect( possString )
    player = possibles[0][0]

    print( player ) 
    prediction = getProjection( player, predWeek )

    print( prediction )
