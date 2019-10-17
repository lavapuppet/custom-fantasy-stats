import requests
import translateStats

def get_Headers(data, titles={}):
    if(type(data)==int):
       titles[data] =  'INT';
    elif(type(data)==float):
        titles[data] =  'FLOAT';
    elif(type(data)==str):
        titles[data] =  'VARCHAR(255)';
    elif(type(data)==bool):
        titles[data] =  'BOOL';
    else:
        titles[data] = 'unknown'; #TODO change to a throw
            
    return titles

def pull_From_Dict(stats, base_dict, titles):
    for key, value in stats.items():
        if key in translateStats.translateDict:
            key = translateStats.translateDict[key]
        if (type(value) == dict):
            base_dict, titles = pull_From_Dict(value, base_dict, titles)
        else:
            if key not in (titles):
                titles = get_Headers(key, titles)
            base_dict[key] = value
    return base_dict, titles

def get_Player_Data(data, titles, player_Data):
    season = data['season']
    week = data['week']
    titles['season'] = 'VARCHAR(255)' 
    titles['week'] = 'INT'
    for player in data['players']:
        base_dict = {}
        base_dict['season'] = season
        base_dict['week'] = week
        base_dict, titles = pull_From_Dict(player,base_dict,titles)
        player_Data.append(base_dict)
    return player_Data, titles    



def test_the_data():
    second_stats = {'cat':'black'}
    stats =[ {'1':'a' , '2':'b' , '3':'c', '4':second_stats}
            , {'5':'a' , '2':'b' , '3':'c', '4':second_stats}]
    return {'players':stats, 'season' :'1', 'week':'2'}


# gets the data
def get_The_Data(season, week, statType, test=False):
    #TODO change this to allow customised string requests with week and season
    paramData = {'season':season,'week': week, 'statType': statType}

    resp = requests.get('https://api.fantasy.nfl.com/v1/players/stats',
                        headers={'Content-Type':'application/json'},
                        params=paramData)
    if resp.status_code != 200:
        # This means something went wrong.
        raise ApiError('GET /tasks/ {}'.format(resp.status_code))
    if resp.status_code == 200:
        print('Success!')
    elif resp.status_code == 404:
        print('Not Found.')
    data = resp.json() #data from our api. This is what we will use.

    titles={};
    playerData = []

    if test == True:
        test_data = test_the_data()
        test_titles={};
        test_players = []
        print(test_data)
        test_data,test_titles = get_Player_Data(test_data,test_titles, test_players)    


    else:
        #getting list of player data headers. We remove season information and
        playerData, titles = get_Player_Data(data, titles, playerData)
        #print(test_players)
        #print(titles)
    return playerData,titles

if __name__== "__main__":
    get_The_Data(1,1,'weekStats', True)

'''
/game/centerpieces
/game/commonleaguetypes
/game/headlines
/game/mockdraftleagues
/game/notifications
/game/promos
/game/teamlogos
/game/ctas
/game/rosterslots
/game/settings
/game/sitemessages
/game/state
/game/stats
/leaderboard
/league/acceptedtrades
/league/draftinfo
/league/draftpicks
/league/feed
/league/feeditemcomments
/league/matchups
/league/messages
/league/messagecomments
/league/playerdetails
/league/playerownership
/league/players
/league/schedule
/league/scheduleclientscoring
/league/settings
/league/standings
/league/teams
/league/team/gamecenter
/league/team/matchup
/league/team/watchlist
/league/team/proposedtrades
/league/team/roster
/league/team/settings
/league/team/waiverrequests
/league/topfreeagents
/league/topplayers
/league/transactions
/league/undroppableplayers
/nfl/schedule
/player/details
/player/advanced
/player/ngs-content
/player/videos
/players/autocomplete
/players/draftclient
/players/fantasystoryvideos
/players/weekliveprojectedstats
/players/weekprojectedstats
/players/weekstats
/players/weektimestats
/players/weekvideos
/registration/drafttimes
/registration/leaguedirectory
/registration/leaguedirectorydraftdates
/sponsoredleaderboard
/user
/user/leagues
/user/leaguesmatchups

#print(data)
#print(resp.headers)
#for stats_item in resp.json():
#    print('{} {}'.format(stats_item['id'], stats_item['summary']))
'''
