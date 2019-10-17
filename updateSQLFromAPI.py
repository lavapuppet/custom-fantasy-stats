import sys

import getAPIFiles
import sqlConnector


if __name__ == '__main__':
    maxWeek = 7 
    if len( sys.argv ) > 2:
        print( "Usage: updateSQLFromAPI.py {weekNumber (default = 7) }" )
    elif len( sys.argv ) == 2:
        maxWeek = int( sys.argv[1] )

    year = '2019'


    # FIXME
    # Handle the data types

    # Set up the DB object
    tableName = 'weekStats'
    db = sqlConnector.sqlConnector()
    if ( db.checkTableExists( tableName ) == True ):
        db.dropTable( 'weekStats' )

    for week in range( 1, maxWeek ):
        print( "Syncing week", week, year )
    #    week = input( "Please enter the week number to download from season 2019:\n" )
        playerData, titles = getAPIFiles.get_The_Data( year, week , 'weekStats')

        # If we haven't already made the table, make it. Otherwise update the headers
        if ( db.checkTableExists( tableName ) == False ):
            db.createTable( tableName, titles )
        else:
            db.updateHeaders( tableName, titles )

        if ( db.checkWeekExists( tableName, week ) == True ):
            print( "Week", week, "already in the table. Deleting old data and entering new" )
            db.deleteWeek( tableName, week )


        #FIXME Need to check that the columns all match nicely

        for player in playerData:
            db.insert( tableName, player, commit=False, debug=False )
        db.commit()

