import getAPIFiles
import sqlConnector



if __name__ == '__main__':
    # FIXME
    # Handle the data types
    week = input( "Please enter the week number to download from season 2019" )
    playerData, titles = getAPIFiles.get_The_Data( '2019', week )

    # Set up the DB object
    db = sqlConnector.sqlConnector()
    tableName = 'weekStats'

    db.createTable( tableName, titles )

    for player in playerData:
        db.insert( tableName, player, commit=False )
    db.commit()

    
