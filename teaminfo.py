import re, urllib2, time, csv, sys
from bs4 import BeautifulSoup, SoupStrainer
#from containers import Team
from datetime import datetime

# CSV File
openFile = open('matches.csv', 'wb')
dataFile = csv.writer(openFile)

# Attributes for HTML Parsing
matchAttr = {'class':'covSmallHeadline'}
rankAttr = {'class':'covSmallHeadline', 'style':'font-weight:normal;width:180px;float:left;text-align:right;'}

# Grabs and reads HTML source from given URL
ua = 'Mozilla/5.0 (X11; Linux x86_64; rv:18.0) Gecko/20100101 Firefox/18.0 (compatible;)' #For User-Agent header
def cooksoup(url):
    request = urllib2.Request(url) # Requests URL
    request.add_header('User-Agent', ua) # Adds User Agent
    response = urllib2.urlopen(request) # Opens URL
    soup = BeautifulSoup(response) # Creates soup
    response.close() #Closes file
    return soup #Returns the HTML

# Fetch all match data for about two years back
dataFile.writerow(['date', 'team 1', 'team 1 score', 'team 1 rank',
            'team 2', 'team 2 score', 'team 2 rank', 'map'])

for pageNum in range(209):
    # Get HTML
    url = 'http://www.hltv.org/?pageid=188&offset=' + str(pageNum*50)
#url = 'http://www.hltv.org/?pageid=188&offset=0'
    soup = cooksoup(url)
    matchInfo = soup.findAll('div', attrs=matchAttr)
    matches = soup.findAll('a', href=re.compile('/\?pageid=188&matchid='))

    for numMatch in range(49):
        # Clean up date
        date = matchInfo[6 + numMatch*5].text
        date = datetime.strptime(date, '%d/%m %y').strftime('%d.%m.%y')
       
        # Clean up team names and scores using Regex
        t1 = re.sub(' \([^)]*\)', '', 
                matchInfo[7 + numMatch*5].text.encode('utf-8'))
        t1 = t1.strip()
        t1Score = re.findall('\([^)]*\)', 
                matchInfo[7 + numMatch*5].text)
        t1Score = int(re.sub('[\(,\)]','', t1Score[0]))

        t2 = re.sub(' \([^)]*\)', '', 
                matchInfo[8 + numMatch*5].text.encode('utf-8'))
        t2 = t2.strip()
        t2Score = re.findall('\([^)]*\)', 
                matchInfo[8 + numMatch*5].text)
        t2Score = int(re.sub('[\(,\)]','', t2Score[0]))

        # Fetch and clean up team ranks
        match = cooksoup('http://www.hltv.org' + matches[numMatch]['href'])
        t1Rank = float(match.findAll('div', rankAttr)[3].text)
        t2Rank = float(match.findAll('div', rankAttr)[4].text)
        
        # Fetch and clean up CS/T scores
        
        # Fetch map and event
        place = matchInfo[9 + numMatch*5].text
        event = matchInfo[10 + numMatch*5].text

        dataFile.writerow([date, t1, t1Score, t1Rank,
            t2, t2Score, t2Rank, place])
        print('Completed match ' + str(numMatch + 1))
    print('----- Completed page ' + str(pageNum + 1) + ' -----')

