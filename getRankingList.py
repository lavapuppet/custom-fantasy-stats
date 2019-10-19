import sqlConnector
import getProjection

positionList = ['QB', 'RB', 'WR', 'TE', 'K', 'DEF']

if __name__=='__main__':

    db = sqlConnector.sqlConnector()
    position = "('WR', 'RB')"
    week = 7
    sqlString = "SELECT DISTINCT name, teamAbbr FROM weekStats WHERE position IN " + position
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
    for name, pts in rankingList:
#        print( name, "\t", round( pts, 2 ) )
        print ( "".join(str(idx).ljust(5)), "".join(name.ljust(col_width)) , round( pts, 2 ) )# for word in row)
        idx += 1

