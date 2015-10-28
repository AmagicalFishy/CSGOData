import urllib2
from bs4 import BeautifulSoup, SoupStrainer

# Grabs and reads HTML source from given URL
ua = 'Mozilla/5.0 (X11; Linux x86_64; rv:18.0) Gecko/20100101 Firefox/18.0 (compatible;)' #For User-Agent header
def CookSoup(url):
    request = urllib2.Request(url) # Requests URL
    request.add_header('User-Agent', ua) # Adds User Agent
    response = urllib2.urlopen(request) # Opens URL
    soup = BeautifulSoup(response) # Creates soup
    response.close() #Closes file
    return soup #Returns the HTML

def BakeSoup(url):
    request = urllib2.Request(url) # Requests URL
    request.add_header('User-Agent', ua) # Adds User Agent
    response = urllib2.urlopen(request) # Opens URL
    html = response.read()
    response.close()
    return html #Returns the HTML

