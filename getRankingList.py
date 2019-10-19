import sqlConnector
import getProjection

positionList = ['QB', 'RB', 'WR', 'TE', 'K', 'DEF']

if __name__=='__main__':

    db = sqlConnector.sqlConnector()
    position = "('QB', 'WR', 'RB', 'TE', 'K', 'DEF')"
    # TODO
    # Tidy this so that one can use % and enter it more nicely, input file?
    roarTeam = "('Lamar Jackson', 'Le''Veon Bell', 'Devonta Freeman', 'T.Y. Hilton', 'Keenan Allen', 'T.J. Hockenson', 'Aaron Jones', 'Greg Zuerlein', 'San Francisco 49ers', 'Matthew Stafford', 'Austin Ekeler', 'D.J. Chark', 'Terry Mclaurin' )"
    ginaTeam = "('Kyler Murray', 'Ezekiel Elliott', 'Cooper Kupp', 'Michael Gallup', 'George Kittle', 'Adam Vinatieri', 'Buffalo Bills', 'Carson Wentz', 'Matt Breida', 'Marlon Mack', 'Calvin Ridley', 'Carolina Panthers')"
    jonnyTeam = "('Matt Ryan', 'Mark Ingram', 'Todd Gurley', 'Julio Jones', 'Robert Woods', 'Evan Engram', 'Alshon Jeffrey', 'Brett Maher', 'Chicago Bears')"
    teamPlayers = roarTeam
    week = 7
    sqlString = "SELECT DISTINCT name, teamAbbr FROM weekStats WHERE name IN " + teamPlayers + " AND position IN " + position
#    sqlString = "SELECT DISTINCT name, teamAbbr FROM weekStats WHERE position IN " + position
    print( sqlString );
    result = db.executeSelect( sqlString )
    #print( result )
    rankingList = {}
    for name in result:
        #print( name[0] )
        rankingList[name[0]] = getProjection.getProjection( name[0], week, db )


#    print( rankingList )
    rankingList = sorted( rankingList.items(), key = lambda kv:(kv[1], kv[0]), reverse=True )


    #TODO would be nice to have team and opposition 
    col_width = 25 #max(len(word) for word in rankingList) + 2  # padding
    idx = 1
    sum = 0
    for name, pts in rankingList:
#        print( name, "\t", round( pts, 2 ) )
        sum += pts
        print ( "".join(str(idx).ljust(5)), "".join(name.ljust(col_width)) , round( pts, 2 ) )# for word in row)
        idx += 1

    print( "total pts:", sum + 18.9 )

