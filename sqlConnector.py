import mysql.connector

# Class to store and maintain a connection to the sql database for our stats
class sqlConnector:
    dbName = 'customFantasyStats'
    dbUser = 'cFSUser'
    #db         database connection
    #cursor     used for passing commands to the db
        
    
    #Initialise the database to point at the customFantasyStats SQL DB and error if it can't
    def __init__( self ):
        try:
            # Open a connection to the db
            self.db = mysql.connector.connect( host="localhost", user=self.dbUser, database=self.dbName )
        except mysql.connector.errors.ProgrammingError as pe:
            print( "Please create the database called", self.dbName, "with user", self.dbUser )
            print( "Error:", pe )
            exit()
        # Set the cursor to the db. This will be used to issue commands to the db
        self.cursor = self.db.cursor()

    # create a table in the db
    def createTable( self, tableName, headerDict ):
        # Create a table with an id as the primary key that is auto incremented
        sqlString = "CREATE TABLE " + tableName + " (id INT AUTO_INCREMENT PRIMARY KEY"
        for header, dataType in headerDict.items():
            sqlString += ", " + header + " " + dataType
        sqlString += ")"
        print( sqlString )
        self.cursor.execute( sqlString )

    def dropTable( self, tableName ):
        self.cursor.execute( "DROP TABLE " + tableName )


    def insert( self, tableName, headerDict, valueList ):
        print( headerDict )    
        print( valueList )
        # Build the insert statement for the given table
        sqlString = "INSERT INTO " + tableName + "("
        # Specify which headers we have values for
        for header in headerDict:
            sqlString += header + ","
        # Delete the final trailing comma
        sqlString = sqlString[:-1]
        # Then the values
        sqlString += ") VALUES ("
        for value in valueList:
            sqlString += "'" + str(value) + "',"
        sqlString = sqlString[:-1]
        sqlString += ")"

        print( sqlString )
        #Finally do the insert
        self.cursor.execute( sqlString )

    def select( self, tableName, headerList ):
        sqlString = "SELECT "
        for header in headerList:
            sqlString += header + ","
        sqlString = sqlString[:-1]
        sqlString += " FROM " + tableName
        self.cursor.execute( sqlString )
        return self.cursor.fetchall()

    # Simply execute the given query if the interface for the functionality has not been provided
    def execute( self, query ):
        self.execute( query )

def sqlType( header ):
    if isinstance( header, str ):
        return "VARCHAR(255)"
    elif isinstance( header, int ):
        return "INT"

if __name__ == "__main__":
    # Initialise a connection to the DB
    db = sqlConnector()
    headerDict = {'name':'VARCHAR(255)', 'team':'VARCHAR(255)',  'number':'INT'}
    valueList = ['Ruairi', 'SEA', 62]
    for head in headerDict:
        print( type( head ) )
    db.createTable( 'testTable', headerDict )
    db.insert( 'testTable', headerDict, valueList )
    selectedData = db.select( 'testTable', ['name', 'number'] )
    print( "selected: ", selectedData )
    db.dropTable( 'testTable' )
    
