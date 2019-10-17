import getAPIFiles
import sqlConnector



if __name__ == '__main__':
    # FIXME
    # Handle the data types
    week = 6 #input( "Please enter the week number to download from season 2019" )
    playerData, titles = getAPIFiles.get_The_Data( '2019', week , 'weekStats')

    # Set up the DB object
    db = sqlConnector.sqlConnector()
    tableName = 'weekStats'

    db.createTable( tableName, titles )

    for player in playerData:
        db.insert( tableName, player, commit=False, debug=False )
    db.commit()

    
