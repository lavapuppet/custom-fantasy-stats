import mysql.connector

# Class to store and maintain a connection to the sql database for our stats
class sqlConnector:
    dbName = 'customFantasyStats'
    dbUser = 'cFSUser'
    tableHeaders = {}
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

    # checks if the table already exists
    def checkTableExists( self, tableName ):
        self.cursor.execute('SHOW TABLES')
        results = self.cursor.fetchall()
        for entry in results:
            for table in entry:
                if tableName == table:
                    return True
        return False        

    # checks if the week already exists in a table
    def checkWeekExists( self, tableName, week ):
        sqlString = "SELECT DISTINCT week FROM " + tableName + " WHERE week = " + str( week )
        self.cursor.execute( sqlString ) 
        results = self.cursor.fetchall()
        if ( results ):
            for weeks in results:
                if weeks[0] == week:
                    return True
        return False

    # Delete all the data from a given week
    def deleteWeek( self, tableName, week ):
        sqlString = "DELETE FROM " + tableName + " WHERE week=" + str( week )
        self.cursor.execute( sqlString )

    # create a table in the db
    def createTable( self, tableName, headerDict, debug = False ):
        # Create a table with an id as the primary key that is auto incremented
        sqlString = "CREATE TABLE " + tableName + " (entry_id INT AUTO_INCREMENT PRIMARY KEY"
        for header, dataType in headerDict.items():
            sqlString += ", `" + header + "` " + dataType
        sqlString += ")"
        if debug:
            print( sqlString )
        self.cursor.execute( sqlString )
        self.tableHeaders[tableName] = headerDict

    def dropTable( self, tableName ):
        self.cursor.execute( "DROP TABLE " + tableName )

    def commit( self ):
        self.db.commit()


    # Insert data into a table.
    # tableName:  table to insert data to
    # insertDict: Dictionary containg the header titles and corresponding data to enter
    # commit:     to HDD only if commit is true -This is useful if you are making a large batch of inserts and only want to commit at the end
    # debug:      print extra debug statements if true
    def insert( self, tableName, insertDict, commit = True, debug = False ):
        # Build the insert statement for the given table
        sqlString = "INSERT INTO " + tableName + " ("
        # Specify which headers we have values for
        valueString = 'VALUES ('
        valueList = []
        for header,value in insertDict.items():
            sqlString += "`" + header + "`,"
            valueString += "%s,"
            valueList.append( str( value ) )
        # Delete the final trailing comma
        sqlString = sqlString[:-1]
        valueString = valueString[:-1]
        # Then the values
        sqlString += ") "
        valueString += ")"
        sqlString += valueString

        if debug:
            print( "debug: insert sql: ", sqlString )
            print( "debug: insert values: ", valueList )
        #Finally do the insert
        self.cursor.execute( sqlString, valueList )
        if commit:
            self.db.commit()
    
    ''' Maybe needed in the future, needs to be tested
    def insertMany( self, tableName, valueDictList ):
        print( headerDict )    
        print( valueList )
        # Build the insert statement for the given table
        sqlString = "INSERT INTO " + tableName + "("
        # Specify which headers we have values for
        for header in valueDictList[0]:
            sqlString += header + ","
        # Delete the final trailing comma
        sqlString = sqlString[:-1]
        # Then the values
        sqlString += ") VALUES ("
        for value in valueDictList[0]:
            sqlString += "%s,"
        sqlString = sqlString[:-1]
        sqlString += ")"

        valList = []
        for row in valueDictList:
            rowVals = []
            for header, value in row.items():
                rowVals.append("'" + str(value) + "',")
            valList.append( rowVals )
        print( valList )
        print( sqlString )
        #Finally do the insert
        #self.cursor.execute( sqlString )
    '''

    # Select some headers from a table
    # tableName:  table to select data from
    # headerList: List of headers to be shown. Note that if only 1 is passed the output is weird, e.g. ('Human',)
    def select( self, tableName, headerList ):
        sqlString = "SELECT "
        for header in headerList:
            sqlString += header + ","
        sqlString = sqlString[:-1]
        sqlString += " FROM " + tableName
        self.cursor.execute( sqlString )
        return self.cursor.fetchall()

    # Check that the headers in a dictionary match with the expected ones for this table and add them if they don't
    def updateHeaders( self, tableName, headerDict ):
        for header, value in headerDict.items():
            if header not in self.tableHeaders[tableName]:
                sqlString = "ALTER TABLE " + tableName + " ADD `" + header + "` " + value;
                self.cursor.execute( sqlString )
                self.tableHeaders[tableName][header] = value

    # Simply execute the given select query if the interface for the functionality has not been provided
    def executeSelect( self, query ):
        self.cursor.execute( query )
        return self.cursor.fetchall()

def sqlType( header ):
    if isinstance( header, str ):
        return "VARCHAR(255)"
    elif isinstance( header, int ):
        return "INT"

if __name__ == "__main__":
    # Initialise a connection to the DB
    db = sqlConnector()

    # Checks if a table already exists before creation    
    if (db.checkTableExists('testTable') == True):
        print( "TEST ERROR IN CHECK EXISTS:" )
        print( "TABLE testTable EXISTS SOMEHOW." )
        db.dropTable( 'testTable' )

    # Use a dictionary of the headers and their types to create a table
    headerDict = {'name':'VARCHAR(255)', 'team':'VARCHAR(255)',  'number':'INT', '88':'VARCHAR(255)', 'week':'INT'}
    db.createTable( 'testTable', headerDict, debug = False )

    # Check if the test table exists
    if ( db.checkTableExists('testTable') == False ):
        print( "TEST ERROR IN CHECK EXISTS:" )
        print( "TABLE testTable DOES NOT EXIST." )
        exit()

    # Checks if week exists in a table before we populate it.
    if ( db.checkWeekExists('testTable', week=6 ) == True ):
        print( "TEST ERROR IN CHECK WEEK EXISTS:" )
        print( "TABLE testTable CONTAINS WEEK 6." )
        db.dropTable( 'testTable' )
        exit()


    # Rows are inserted using a dictionary containing the column titles and the values corresponding
    valueList = [{'name':'Human1', 'number':62, 'week':4},
                 {'name':'Person2', 'number':13, 'team':'CHI'},
                 {'name':'Lady3', 'number':449, 'week':6},
                 {'name':'Man4', 'number':86, 'team':'PAT'}]
                
    # We pass false to indicate it should not be committed to HDD until later
    for valueDict in valueList:
        db.insert( 'testTable', valueDict, commit=False, debug=False )
    # Use the commit function to save to HDD
    db.commit()

    # Checks if a week has been entered in a specific table 
    if (db.checkWeekExists('testTable', week=6 ) == False):
        print( "TEST ERROR IN CHECK WEEK EXISTS:" )
        print( "TABLE testTable IS MISSING DATA." )
        db.dropTable( 'testTable' )
        exit()

    # Add a new column with name face
    headerDict = {'name':'VARCHAR(255)', 'team':'VARCHAR(255)',  'face':'VARCHAR(255)', '88':'VARCHAR(255)', 'week':'INT'}
    db.updateHeaders( 'testTable', headerDict )

    # Delete all entries with week=4
    db.deleteWeek( 'testTable', 4 )

    # Simple selects can be issued by passing a list of the desired headers
    selectedData = db.select( 'testTable', ['name', 'number', 'team'] )
    expectData = [('Person2', 13, 'CHI'), ('Lady3', 449, None), ('Man4', 86, 'PAT')] 
    if ( selectedData != expectData ):
        print( "TEST ERROR IN SIMPLE SELECT:")
        print( "Expected:", expectData )
        print( "Got:     ", selectedData )
        db.dropTable( 'testTable' )
        exit()

    # More complicated selects should use the execute command
    executeString = "SELECT name, team, face FROM testTable WHERE team IS NOT NULL"
    selectedData = db.executeSelect( executeString )
    expectData = [('Person2', 'CHI', None), ('Man4', 'PAT', None)]
    if ( selectedData != expectData ):
        print( "TEST ERROR IN COMPLICATED SELECT:")
        print( "Expected:", expectData )
        print( "Got:     ", selectedData )
        print( "For sql:", executeString )
        db.dropTable( 'testTable' )
        exit()

    # Drop table is provided if neccessary. In this case delete the table after testing
    # May need to be done manually if test fails
    db.dropTable( 'testTable' )

    
    print( "TEST SUCCESS" )

