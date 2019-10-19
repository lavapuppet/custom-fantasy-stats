# custom-fantasy-stats
Our personal NFL information aggregator


-- Uses a MySQL database to store data from the NFLFantasy API and do stats

1. Set up a MySQL DB called customFantasyStats. This should have a user cFSUser with no password.
 The python code will build the tables necessary to store the stats once this is done.

2. Ensure that small groupings are allowed on your sql server installation.
 To do this, modify:
    sudo vim /etc/my.cnf
 and add the lines, or at least ensure the sql-mode variable is set as below:
    [mysqld]
    sql-mode=select_replace

3. Install mysql-connector for python: sudo python3 -m pip install mysql-connector

4. Install requests for python: sudo python3 -m pip install requests



NFL Fantasy API Documentation:
https://api.fantasy.nfl.com/v2/docs/



Running:

Start with 'updateSQLFromAPI.py' and specify the week number up to which you would like to pull. e.g.:
$ python3 updateSQLFromAPI.py 7

You will now have a database of players weekly stats which you can peruse at your leisure

To run pre-built prediction models specify the player name (SQL like string matching allowed) and week number to predict for. Defaults to 2019 e.g.:
$ python3 getProjection.py "%Julio%" 7
produces output like:
team prediction: 41.77444383992008
Julio Jones predction 15.804357952350873






#TODOs
Build position rankings for a week
Build rankings for rest of season!!
Make it easier to build different prediction models

