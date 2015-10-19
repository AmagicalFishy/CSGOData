import re
import urllib2
import time
from bs4 import BeautifulSoup, SoupStrainer
from containers import Team
from datetime import datetime

#Attributes for HTML Parsing
teamRankAttr = {'class':'tooltip'} #span
teamNameAttr = {'class':'teamNameHolder'} #div
gameWinnersAttr = {'class':'btn-url'} #input
gameScoreAttr = {'class':'roundset totals'} #div
homeScoreAttr = {'class':'home score'} #span
awayScoreAttr = {'class':'away score'} #span
mapNameAttr = {'class':'map-image'} #div
eventAttr = {'align':'center'} #legend

#Grabs and reads HTML source from given URL
ua = 'Mozilla/5.0 (X11; Linux x86_64; rv:18.0) Gecko/20100101 Firefox/18.0 (compatible;)' #For User-Agent header
def cooksoup(url):
    request = urllib2.Request(url) #Requests URL
    request.add_header('User-Agent',ua) #Adds User Agent
    response = urllib2.urlopen(request) #Opens URL
    soup = BeautifulSoup(response) #Creates soup
    response.close() #Closes file
    return soup #Returns the HTML


#Input GOSU-Gamers team ID (the last clause on the team's profile page)
def teaminfo(teamID):
    teamURL = str('http://www.gosugamers.net/counterstrike/teams/'
            + str(teamID))
    teamNum = re.split('[\-]', teamID)[0]

    soup = cooksoup(teamURL) #HTML

    #Regex Strings
    rexMatch = '^match-row-' + teamNum + '-' + '\d{1}' + '-l' #Match Regex

    #Get the links to the recent matches and store them in a list
    recentMatchContainers = soup.findAll('div', id=re.compile(rexMatch))
    numMatches = len(recentMatchContainers)
    matchLink = ['filler']*numMatches
    for ii in range(numMatches):
        matchLink[ii] = 'http://www.gosugamers.net' \
                + recentMatchContainers[ii].findAll('a')[0].attrs['href']

    #HTML Parsing
    teamRank = int(soup('span', attrs=teamRankAttr)[0].text.replace(',',''))
    teamName = str(soup('div', attrs=teamNameAttr)[0].text)
    teamName = re.split(' - Team Overview', teamName)[0].strip('\n\n ')

    thisTeam = Team(teamName, teamRank)

    ## Recent Match Statistics ##
    #(1) Date of Match
    #(2) Opponent Name
    #(3) Opponent Rank
    #(4) Map
    #(5) This team's score
    #(6) Opponent team's score

    #Get statistics and fill class
    for ii,link in enumerate(matchLink):
        print("Processing Game: " + str(ii+1) + "/" + str(len(matchLink)))
        soup = cooksoup(link) #Read HTML

        #Get Opponent Name
        opponents = soup.findAll('div', attrs={'class':'match-opponents'})
        for entry in opponents[0].findAll('a'):
            if entry.text == teamName:
                pass
            else:
                opponentName = str(entry.text)
                break

        #Get Date
        try:
            datime = soup.findAll('p', attrs={'class':'datetime'})[0].text.strip()
            datime = datime.strip(' CET')
            datime = datetime.strptime(datime, '%B %d, %A, %H:%M').strftime('%m/%d')
        except:
            print("No date found")
            datime = ""

        #Get Event
        event = soup.find('legend', attrs=eventAttr)
        event = event.find('a').text

        #Get Scores, Winner, and  Map Names for All Games

        #Fetches winner of each game to contain only the winners
        gameWinners = soup.findAll('input', attrs=gameWinnersAttr)
        for ii, entry in enumerate(gameWinners):
            try:
                gameWinners[ii] = re.split('/', entry['value'])[2]
            except:
                gameWinners[ii] = "Tie Game"

        gameScores = soup.findAll('div', attrs=gameScoreAttr)

        #len(gameScores) is also the number of games this match has (for
        #example, it'd be 3 if it's a Bo3 match.
        for jj in range(len(gameWinners)):
            thisTeam.add_game()
            thisTeam.recentGames[-1]['event'] = event
            thisTeam.recentGames[-1]['date'] = datime
            thisTeam.recentGames[-1]['opponent'] = opponentName

            matchInfo = soup.findAll('div',
                    attrs={'id':'match-game-tab-'+ str(jj) +'-content'})

            #Get Scores
            try:
                score1 = gameScores[jj].findAll('span',attrs=homeScoreAttr)
                score2 = gameScores[jj].findAll('span',attrs=awayScoreAttr)
                score1 = int(score1[0].text)
                score2 = int(score2[0].text)

            except:
                score1 = None
                score2 = None

            winner = max(score1, score2)
            loser = min(score1, score2)

            #Set scores appropriately
            if gameWinners[jj] == teamID:
                thisTeam.recentGames[-1]['teamScore'] = winner
                thisTeam.recentGames[-1]['oppScore'] = loser

            else:
                thisTeam.recentGames[-1]['teamScore'] = loser
                thisTeam.recentGames[-1]['oppScore'] = winner

            #Get Names of Maps
            mapNames = soup.findAll('div',attrs=mapNameAttr)
            try:
                thisTeam.recentGames[-1]['map'] = mapNames[jj].find('label').text
            except:
                thisTeam.recentGames[-1]['map'] = "No Info."
            
            #Get Opponent's Current Rank
            #Follow link to opponents name, parse HTML, add rank
            oppLink = soup.find('h3',text=opponentName).find('a')['href']
            oppSoup = cooksoup('http://www.gosugamers.net' + oppLink)
            oppRank = int(oppSoup('span', attrs=teamRankAttr)[0].text.replace(',',''))
            thisTeam.recentGames[-1]['oppRank'] = oppRank

        #time.sleep(3)

    return thisTeam

#For Debugging Purposes
if __name__ == "__main__":
    teamID = raw_input("GosuGamers TeamID?\n")
    Team = teaminfo(teamID)
