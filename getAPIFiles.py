import requests


def get_Player_Data(data):
   return
    
def get_Headers(data, titles={}):
    for topics in data:
        #print(topics)
        if(type(topics)==dict):
            for keys in data[topics][0] :
                print((keys)) 
                if(type(data[topics][0][keys])==int):
                   titles[keys] =  'INT';
                elif(type(data[topics][0][keys])==float):
                    titles[keys] =  'FLOAT';
                elif(type(data[topics][0][keys])==str):
                    titles[keys] =  'VARCHAR';
                elif(type(data[topics][0][keys])==bool):
                    titles[keys] =  'BOOL';
                elif(type(data[topics][0][keys])==dict):
                    titles = get_Headers(data[topics][0][keys],titles);
                else:
                    titles[keys] = 'unknown';
        else:
                if(type(data[topics])==int):
                   titles[keys] =  'INT';
                elif(type(data[topics][0])==float):
                    titles[keys] =  'FLOAT';
                elif(type(data[topics][0])==str):
                    titles[keys] =  'VARCHAR';
                elif(type(data[topics][0])==bool):
                    titles[keys] =  'BOOL';
                elif(type(data[topics][0])==dict):
                    titles = get_Headers(data[topics][0][keys],titles);
                else:
                    titles[keys] = 'unknown';
            
    return titles

def get_The_Data():
    resp = requests.get('https://api.fantasy.nfl.com/v1/players/stats',
                        headers={'Content-Type':'application/json'})
    if resp.status_code != 200:
        # This means something went wrong.
        raise ApiError('GET /tasks/ {}'.format(resp.status_code))
    if resp.status_code == 200:
        print('Success!')
    elif resp.status_code == 404:
        print('Not Found.')
    data = resp.json() #data from our api. This is what we will use.

    titles={};

    #getting list of player data headers. We remove season information and
    get_Player_Data(data)

if __name__== "__main__":
    get_The_Data()

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
