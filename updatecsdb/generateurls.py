import re, csv
from cooksoup import CookSoup

# File where page URLs are stored
uFile = open('matchurls.csv', 'wb')
urlFile = csv.writer(uFile)

url = 'http://www.hltv.org/?pageid=188&offset=0' # Initial page URL
onPage = 0 # Page count
pageIndex = 1 #
print("Getting last page. This may take a while...")

while True:
    soup = CookSoup(url) # Get HTML from URL
    # Get 'next page' URLs
    urls = soup.findAll('a', {'href':re.compile('.*pageid=188.*offset=')})
    # Check if this is the last page
    if int(urls[len(urls) - 1].text) < onPage: break

    onPage = int(urls[len(urls) - 1].text) # Current page
    # Current URL
    url = 'http://www.hltv.org' + urls[len(urls) - 1]['href']
    pageIndex = pageIndex + 1 # Number of URLs fetched
    # Print out status
    if pageIndex % 15 == 0: print("On page " + str(onPage))

print("Finished.\nWriting URLs to file...")

# Write URLs to file
for ii in range(onPage):
    urlFile.writerow(['http://www.hltv.org/?pageid=188&offset=' + str(ii*50)])
    if ii % 25 == 0: print("Writing page " + str(ii))

uFile.close()
