import sys

import getAPIFiles
import sqlConnector


if __name__ == '__main__':
    if len( sys.argv ) > 2:
        print( "Usage: updateSQLFromAPI.py {weekNumber (default = 6) }" )
    elif len( sys.argv ) == 2:
        week = int( sys.argv[1] )
    else:
        week = 6

    year = '2019'

    print( "Syncing week", week, year )

    # FIXME
    # Handle the data types
#    week = input( "Please enter the week number to download from season 2019:\n" )
    playerData, titles = getAPIFiles.get_The_Data( year, week , 'weekStats')

    # Set up the DB object
    db = sqlConnector.sqlConnector()
    tableName = 'weekStats'

    # If we haven't already made the table, make it
    if ( db.checkTableExists( tableName ) == False ):
        db.createTable( tableName, titles )

    if ( db.checkWeekExists( tableName, week ) == True ):
        print( "Week", week, "already in the table. Deleting old data and entering new" )
        db.deleteWeek( tableName, week )

    #FIXME Need to check that the columns all match nicely

    for player in playerData:
        db.insert( tableName, player, commit=False, debug=False )
    db.commit()

